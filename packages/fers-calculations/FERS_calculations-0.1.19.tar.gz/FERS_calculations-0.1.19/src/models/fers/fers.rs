
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use std::collections::{BTreeMap, HashMap};
use nalgebra::DMatrix;
use std::collections::HashSet;
// use csv::Writer;
// use std::error::Error;
use crate::models::members::{material::Material, section::Section, memberhinge::MemberHinge, shapepath::ShapePath};
use crate::models::members::memberset::MemberSet;
use crate::models::loads::loadcase::LoadCase;
use crate::models::loads::loadcombination::LoadCombination;
use crate::models::imperfections::imperfectioncase::ImperfectionCase;
use crate::models::results::displacement::NodeDisplacement;
use crate::models::results::forces::{MemberForce, NodeForces, ReactionForce};
use crate::models::results::memberresultmap::MemberResultMap;
use crate::models::results::results::Results;
use crate::models::results::resultssummary::ResultsSummary;
use crate::models::settings::settings::Settings;
use crate::models::supports::nodalsupport::NodalSupport;

use crate::functions::load_assembler::{assemble_nodal_loads, assemble_nodal_moments, assemble_distributed_loads};


#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct FERS {
    pub member_sets: Vec<MemberSet>,
    pub load_cases: Vec<LoadCase>,
    pub load_combinations: Vec<LoadCombination>,
    pub imperfection_cases: Vec<ImperfectionCase>,
    pub settings: Settings, 
    pub results: Option<Results>,
    pub memberhinges: Option<Vec<MemberHinge>>,
    pub materials: Vec<Material>,
    pub sections: Vec<Section>,
    pub nodal_supports: Vec<NodalSupport>, 
    pub shape_paths: Option<Vec<ShapePath>>,
}

impl FERS {
    // Function to build lookup maps from Vec<Material>, Vec<Section>, and Vec<MemberHinge>
    pub fn build_lookup_maps(
        &self
    ) -> (
        HashMap<u32, &Material>,
        HashMap<u32, &Section>,
        HashMap<u32, &MemberHinge>,
        HashMap<u32, &NodalSupport>
    ) {
        let material_map: HashMap<u32, &Material> = self.materials.iter().map(|m| (m.id, m)).collect();
        let section_map: HashMap<u32, &Section> = self.sections.iter().map(|s| (s.id, s)).collect();
        let memberhinge_map: HashMap<u32, &MemberHinge> = self.memberhinges.iter().flatten().map(|mh| (mh.id, mh)).collect();
        let support_map: HashMap<u32, &NodalSupport> = self.nodal_supports.iter().map(|s| (s.id, s)).collect();
        
        (material_map, section_map, memberhinge_map, support_map)
    }

    pub fn get_member_count(&self) -> usize {
        self.member_sets
            .iter()
            .map(|ms| ms.members.len())
            .sum()
    }

    pub fn assemble_global_stiffness_matrix(&self) -> Result<DMatrix<f64>, String> {
        self.validate_node_ids()?;

        let (material_map, section_map, _memberhinge_map, _support_map) = self.build_lookup_maps();

        let num_dofs: usize = self.member_sets.iter()
            .flat_map(|ms| ms.members.iter())
            .flat_map(|m| vec![m.start_node.id, m.end_node.id])
            .max()
            .unwrap_or(0) as usize * 6; // 6 DOFs per node in 3D

        let mut k_global = DMatrix::<f64>::zeros(num_dofs, num_dofs);

        for member_set in &self.member_sets {
            for member in &member_set.members {
                if let Some(k_local) = member.calculate_stiffness_matrix_3d(&material_map, &section_map) {
                    Self::print_matrix(&k_local, &format!("Local Stiffness Matrix for Member {}", member.id));

                    let det = k_local.determinant();
                    log::debug!("Determinant of local stiffness matrix: {}", det);

                    // 2. Calculate the transformation matrix
                    let t_matrix = member.calculate_transformation_matrix_3d();
                    Self::print_matrix(&t_matrix, &format!("Transformation Matrix for Member {}", member.id));
                    // let csv_file = format!("transformation_matrix_member_{}.csv", member.id);
                    // if let Err(e) = Self::save_matrix_to_csv(&t_matrix, &csv_file) {
                    //     elog::debug!("Failed to save transformation matrix for Member {}: {}", member.id, e);
                    // } else {
                    //     log::debug!("Transformation matrix saved to '{}'", csv_file);
                    // }


                    // 3. Transform local stiffness to global coordinates
                    let k_global_transformed = t_matrix.transpose() * k_local * t_matrix;
                    Self::print_matrix(&k_global_transformed, &format!("Transformed Stiffness Matrix for Member {}", member.id));

                    // 4. Add to global stiffness matrix
                    let start_index: usize = (member.start_node.id as usize - 1) * 6;
                    let end_index: usize = (member.end_node.id as usize - 1) * 6;

                    for i in 0..6 {
                        for j in 0..6 {
                            k_global[(start_index + i, start_index + j)] += k_global_transformed[(i, j)];
                            k_global[(start_index + i, end_index + j)] += k_global_transformed[(i, j + 6)];
                            k_global[(end_index + i, start_index + j)] += k_global_transformed[(i + 6, j)];
                            k_global[(end_index + i, end_index + j)] += k_global_transformed[(i + 6, j + 6)];
                        }
                    }
                }
            }
        }

        Ok(k_global)

    }

    pub fn validate_node_ids(&self) -> Result<(), String> {
        // Collect all node IDs in a HashSet for quick lookup
        let mut node_ids: HashSet<u32> = HashSet::new();

        // Populate node IDs from all members
        for member_set in &self.member_sets {
            for member in &member_set.members {
                node_ids.insert(member.start_node.id);
                node_ids.insert(member.end_node.id);
            }
        }

        // Ensure IDs start at 1 and are consecutive
        let max_id = *node_ids.iter().max().unwrap_or(&0);
        for id in 1..=max_id {
            if !node_ids.contains(&id) {
                return Err(format!("Node ID {} is missing. Node IDs must be consecutive starting from 1.", id));
            }
        }

        Ok(())
    }


    pub fn apply_boundary_conditions(&self, k_global: &mut DMatrix<f64>) {
        // Build the support mapping from support id to &NodalSupport.
        // This maps the nodal support definitions provided in FERS.
        let support_map: HashMap<u32, &NodalSupport> = self
            .nodal_supports
            .iter()
            .map(|support| (support.id, support))
            .collect();

        // Create a set to keep track of node IDs that have already had their boundary conditions applied.
        let mut applied_nodes: HashSet<u32> = HashSet::new();

        // Loop over each memberset and each member within
        for member_set in &self.member_sets {
            for member in &member_set.members {
                // Process both the start and end nodes of the member.
                for node in [&member.start_node, &member.end_node] {
                    // Check if we've already applied the BC for this node.
                    if applied_nodes.contains(&node.id) {
                        continue;
                    }

                    // Only apply a BC if the node has a nodal support assigned.
                    if let Some(support_id) = node.nodal_support {
                        // Attempt to retrieve the corresponding nodal support from the support_map.
                        if let Some(support) = support_map.get(&support_id) {
                            self.constrain_dof(k_global, node.id, support);
                            applied_nodes.insert(node.id);
                        }
                    }
                }
            }
        }
    }


    // Helper function to apply constraints based on support
    fn constrain_dof(&self, k_global: &mut DMatrix<f64>, node_id: u32, support: &NodalSupport) {
        let dof_start = (node_id as usize - 1) * 6;

        // Constrain translational DOFs based on displacement conditions
        for (axis, condition) in &support.displacement_conditions {
            let dof = match axis.as_str() {
                "X" => 0,  // X translation
                "Y" => 1,  // Y translation
                "Z" => 2,  // Z translation
                _ => continue,
            };
            match condition.as_str() {
                "Fixed" => self.constrain_single_dof(k_global, dof_start + dof),
                "Free"  => {
                    // DOF is free, so do nothing
                },
                // Optionally handle other conditions (e.g., "Pinned") here
                _ => continue,
            }
        }

        // Constrain rotational DOFs based on rotation conditions
        for (axis, condition) in &support.rotation_conditions {
            let dof = match axis.as_str() {
                "X" => 3,  // X rotation
                "Y" => 4,  // Y rotation
                "Z" => 5,  // Z rotation
                _ => continue,
            };
            match condition.as_str() {
                "Fixed" => self.constrain_single_dof(k_global, dof_start + dof),
                "Free"  => {
                    // Rotation is free, so leave it unmodified.
                },
                _ => continue,
            }
        }
    }

    // Helper function to apply constraints to a single DOF by modifying k_global
    fn constrain_single_dof(&self, k_global: &mut DMatrix<f64>, dof_index: usize) {
        // Zero out the row and column for this constrained DOF
        for j in 0..k_global.ncols() {
            k_global[(dof_index, j)] = 0.0;
        }
        for i in 0..k_global.nrows() {
            k_global[(i, dof_index)] = 0.0;
        }
        k_global[(dof_index, dof_index)] = 1e20;  // Large value to simulate constraint
    }

    pub fn assemble_load_vector_for_case(&self, load_case_id: u32) -> DMatrix<f64> {
        let num_dofs = self.member_sets.iter()
            .flat_map(|ms| ms.members.iter())
            .flat_map(|m| vec![m.start_node.id, m.end_node.id])
            .max()
            .unwrap_or(0) as usize * 6;
        let mut f = DMatrix::<f64>::zeros(num_dofs, 1);
    
        if let Some(load_case) = self.load_cases.iter().find(|lc| lc.id == load_case_id) {
            assemble_nodal_loads(load_case, &mut f);
            assemble_nodal_moments(load_case, &mut f);
            assemble_distributed_loads(load_case, &self.member_sets, &mut f, load_case_id);
        }
        f
    }
    pub fn solve_for_load_case(&mut self, load_case_id: u32) -> Result<Results, String> {
        log::debug!("Validating node IDs...");
        self.validate_node_ids()?;

        log::debug!("Assembling global stiffness matrix...");
        let original_k = self.assemble_global_stiffness_matrix()?; 
        let mut k_global = original_k.clone();
        Self::print_matrix(&k_global, "Global Stiffness Matrix");

        log::debug!("Applying boundary conditions...");
        self.apply_boundary_conditions(&mut k_global);
        Self::print_matrix(&k_global, "Global Stiffness Matrix after Boundary Conditions");

        log::debug!("Assembling load vector for load case ID: {}", load_case_id);
        let f = self.assemble_load_vector_for_case(load_case_id);
        Self::print_matrix(&f, &format!("Load Vector for Load Case {}", load_case_id));

        let det = k_global.determinant();
        log::debug!("Determinant of global stiffness matrix: {}", det);

        log::debug!("Solving for displacements...");
        let u: nalgebra::Matrix<f64, nalgebra::Dyn, nalgebra::Dyn, nalgebra::VecStorage<f64, nalgebra::Dyn, nalgebra::Dyn>> = match k_global.clone().lu().solve(&f) {
            Some(solution) => solution,
            None => return Err("Global stiffness matrix is singular or near-singular.".into()),
        };
        Self::print_matrix(&u, "Displacement Vector");

        log::debug!("Calculating reaction forces...");
        let reaction_forces = &original_k * &u - &f;
        Self::print_matrix(&reaction_forces, "Reaction Forces");

        log::debug!("Storing results...");

        let (member_forces, member_minimums, member_maximums) = self.extract_member_forces();

        let results = Results {
            name: format!("Load Case {}", load_case_id),
            result_type: format!("Load Case {}", load_case_id),
            displacement_nodes: self.extract_displacements(&u),
            reaction_forces: self.extract_reaction_forces(&reaction_forces),
            member_forces: member_forces,
            summary: ResultsSummary {
                total_displacements: self.member_sets.iter().map(|ms| ms.members.len()).sum(),
                total_reaction_forces: self.nodal_supports.len(),
                total_member_forces: self.member_sets.iter().map(|ms| ms.members.len()).sum(),
            },
            member_minimums: Some(member_minimums),
            member_maximums: Some(member_maximums),
        };

        self.results = Some(results.clone());

        Ok(results)
    }




    #[allow(dead_code)]
    fn print_matrix(matrix: &DMatrix<f64>, name: &str) {
        if log::log_enabled!(log::Level::Debug) {
            println!("{} ({}x{}):", name, matrix.nrows(), matrix.ncols());
            for i in 0..matrix.nrows() {
                for j in 0..matrix.ncols() {
                    print!("{:10.2} ", matrix[(i, j)]);
                }
                println!();
            }
            println!();
        }
    }

    // fn save_matrix_to_csv(matrix: &DMatrix<f64>, file_path: &str) -> Result<(), Box<dyn Error>> {
    //     let mut wtr = Writer::from_path(file_path)?;
    
    //     for i in 0..matrix.nrows() {
    //         let row: Vec<String> = (0..matrix.ncols())
    //             .map(|j| format!("{:.6}", matrix[(i, j)])) // Format each element to 6 decimal places
    //             .collect();
    //         wtr.write_record(&row)?;
    //     }
    
    //     wtr.flush()?; // Ensure all data is written to the file
    //     log::debug!("Matrix saved to '{}'", file_path);
    
    //     Ok(())
    // }

    fn extract_displacements(&self, u: &DMatrix<f64>) -> BTreeMap<u32, NodeDisplacement> {
        // Collect unique node IDs from all members
        let mut unique_node_ids: HashSet<u32> = HashSet::new();
        for member_set in &self.member_sets {
            for member in &member_set.members {
                unique_node_ids.insert(member.start_node.id);
                unique_node_ids.insert(member.end_node.id);
            }
        }
    
        // Map each unique node ID to its corresponding displacements from u
        unique_node_ids
            .into_iter()
            .map(|node_id| {
                let dof_start = (node_id as usize - 1) * 6;
                (
                    node_id,
                    NodeDisplacement {
                        dx: u[(dof_start, 0)],
                        dy: u[(dof_start + 1, 0)],
                        dz: u[(dof_start + 2, 0)],
                        rx: u[(dof_start + 3, 0)],
                        ry: u[(dof_start + 4, 0)],
                        rz: u[(dof_start + 5, 0)],
                    },
                )
            })
            .collect()
    }

    fn extract_reaction_forces(&self, r: &DMatrix<f64>) -> Vec<ReactionForce> {
        self.nodal_supports
            .iter()
            .enumerate()
            .map(|(support_id, support)| {
                let dof_start = (support_id) * 6;
                ReactionForce {
                    support_id: support.id,
                    fx: r[(dof_start, 0)],
                    fy: r[(dof_start + 1, 0)],
                    fz: r[(dof_start + 2, 0)],
                    mx: r[(dof_start + 3, 0)],
                    my: r[(dof_start + 4, 0)],
                    mz: r[(dof_start + 5, 0)],
                }
            })
            .collect()
    }

    fn extract_member_forces(&self) -> (Vec<MemberForce>, MemberResultMap, MemberResultMap) {
        let mut member_minimums = MemberResultMap {
            data: HashMap::new(),
        };
        let mut member_maximums = MemberResultMap {
            data: HashMap::new(),
        };
    
        // Collect forces for each member
        let member_forces: Vec<MemberForce> = self
            .member_sets
            .iter()
            .flat_map(|ms| ms.members.iter())
            .map(|member| {
                // Placeholder for actual force computations
                let start_forces = NodeForces {
                    fx: 0.0, // Replace with computed value
                    fy: 0.0,
                    fz: 0.0,
                    mx: 0.0,
                    my: 0.0,
                    mz: 0.0,
                };
    
                let end_forces = NodeForces {
                    fx: 0.0, // Replace with computed value
                    fy: 0.0,
                    fz: 0.0,
                    mx: 0.0,
                    my: 0.0,
                    mz: 0.0,
                };
    
                let member_force = MemberForce {
                    member_id: member.id,
                    start_node_forces: start_forces.clone(),
                    end_node_forces: end_forces.clone(),
                };
    
                // Calculate min and max forces for this member
                let mut min_values = HashMap::new();
                let mut max_values = HashMap::new();
    
                for (key, start_value, end_value) in [
                    ("fx", start_forces.fx, end_forces.fx),
                    ("fy", start_forces.fy, end_forces.fy),
                    ("fz", start_forces.fz, end_forces.fz),
                    ("mx", start_forces.mx, end_forces.mx),
                    ("my", start_forces.my, end_forces.my),
                    ("mz", start_forces.mz, end_forces.mz),
                ] {
                    min_values.insert(key.to_string(), start_value.min(end_value));
                    max_values.insert(key.to_string(), start_value.max(end_value));
                }
    
                let member_id = format!("Member {}", member.id);
                member_minimums.data.insert(member_id.clone(), min_values);
                member_maximums.data.insert(member_id, max_values);
    
                member_force
            })
            .collect();
    
        (member_forces, member_minimums, member_maximums)
    }

    pub fn save_results_to_json(fers_data: &FERS, file_path: &str) -> Result<(), std::io::Error> {
        let json = serde_json::to_string_pretty(fers_data)?; // Serialize FERS struct to JSON
        std::fs::write(file_path, json) // Write the JSON to the specified file
    }


}