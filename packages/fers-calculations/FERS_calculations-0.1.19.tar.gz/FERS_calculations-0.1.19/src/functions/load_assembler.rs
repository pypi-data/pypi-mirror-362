use nalgebra::DMatrix;
use crate::models::loads::loadcase::LoadCase;
use crate::models::members::memberset::MemberSet;
use crate::functions::helpers::get_dof_indices;  

/// Assembles the nodal loads into the global load vector.
pub fn assemble_nodal_loads(load_case: &LoadCase, f: &mut DMatrix<f64>) {
    for nodal_load in &load_case.nodal_loads {
        let node_id = nodal_load.node as usize;
        let (fx_index, fy_index, fz_index, _, _, _) = get_dof_indices(node_id);
        if nodal_load.direction.0 != 0.0 {
            f[(fx_index, 0)] += nodal_load.magnitude * nodal_load.direction.0;
        }
        if nodal_load.direction.1 != 0.0 {
            f[(fy_index, 0)] += nodal_load.magnitude * nodal_load.direction.1;
        }
        if nodal_load.direction.2 != 0.0 {
            f[(fz_index, 0)] += nodal_load.magnitude * nodal_load.direction.2;
        }
    }
}

/// Assembles the nodal moments into the global load vector.
pub fn assemble_nodal_moments(load_case: &LoadCase, f: &mut DMatrix<f64>) {
    for nodal_moment in &load_case.nodal_moments {
        let node_id = nodal_moment.node as usize;
        let (_, _, _, rx_index, ry_index, rz_index) = get_dof_indices(node_id);
        if nodal_moment.direction.0 != 0.0 {
            f[(rx_index, 0)] += nodal_moment.magnitude * nodal_moment.direction.0;
        }
        if nodal_moment.direction.1 != 0.0 {
            f[(ry_index, 0)] += nodal_moment.magnitude * nodal_moment.direction.1;
        }
        if nodal_moment.direction.2 != 0.0 {
            f[(rz_index, 0)] += nodal_moment.magnitude * nodal_moment.direction.2;
        }
    }
}

/// Assembles the distributed loads into the global load vector.
/// The function uses member sets to locate the member for each distributed load.
pub fn assemble_distributed_loads(
    load_case: &LoadCase,
    member_sets: &[MemberSet],
    f: &mut DMatrix<f64>,
    load_case_id: u32,
) {
    for distributed_load in &load_case.distributed_loads {
        if distributed_load.load_case != load_case_id {
            continue;
        }

        // Find the member corresponding to the distributed load
        let member_id = distributed_load.member.id;        // grab the u32
        let member_opt = member_sets.iter()
            .flat_map(|ms| ms.members.iter())
            .find(|member| member.id == member_id);

        if let Some(member) = member_opt {
            let l_segment = distributed_load.end_pos - distributed_load.start_pos;
            let force_equiv = distributed_load.magnitude * l_segment / 2.0;
            let moment_equiv = distributed_load.magnitude * l_segment * l_segment / 12.0;

            // Apply loads for start node
            let start_node_id = member.start_node.id as usize;
            let (start_fx, start_fy, start_fz, start_rx, start_ry, start_rz) =
                get_dof_indices(start_node_id);
            f[(start_fx, 0)] += force_equiv * distributed_load.direction.0;
            f[(start_fy, 0)] += force_equiv * distributed_load.direction.1;
            f[(start_fz, 0)] += force_equiv * distributed_load.direction.2;
            f[(start_rx, 0)] += moment_equiv * distributed_load.direction.0;
            f[(start_rz, 0)] += moment_equiv * distributed_load.direction.1;
            f[(start_ry, 0)] += moment_equiv * distributed_load.direction.2;

            // Apply loads for end node (with negative moment contribution)
            let end_node_id = member.end_node.id as usize;
            let (end_fx, end_fy, end_fz, end_rx, end_ry, end_rz) =
                get_dof_indices(end_node_id);
            f[(end_fx, 0)] += force_equiv * distributed_load.direction.0;
            f[(end_fy, 0)] += force_equiv * distributed_load.direction.1;
            f[(end_fz, 0)] += force_equiv * distributed_load.direction.2;
            f[(end_rx, 0)] -= moment_equiv * distributed_load.direction.0;
            f[(end_rz, 0)] -= moment_equiv * distributed_load.direction.1;
            f[(end_ry, 0)] -= moment_equiv * distributed_load.direction.2;
        }
    }
}