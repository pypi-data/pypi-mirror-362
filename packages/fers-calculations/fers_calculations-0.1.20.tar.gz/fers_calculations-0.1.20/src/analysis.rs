// src/analysis.rs

use crate::models::fers::fers::FERS;
use serde_json;
use std::fs;
use std::path::Path;   
use std::io;     
use nalgebra::DMatrix;

/// Perform analysis on the given JSON input string.
///
/// This function handles:
/// 1) Parsing the JSON into a FERS struct.
/// 2) Identifying the first load case.
/// 3) Performing structural analysis (solve_for_load_case).
/// 4) Optionally printing results.
/// 5) Saving results to an output file (analysis_results.json).
///
/// Returns an `Ok(String)` with a success message, or an `Err(String)` on failure.
pub fn calculate_from_json_internal(json_data: &str) -> Result<String, String> {
    // 1) Parse the JSON into a FERS struct
    let mut fers_data: FERS = match serde_json::from_str(json_data) {
        Ok(fers_data) => fers_data,
        Err(e) => return Err(format!("JSON was not well-formatted: {}", e)),
    };

    // 2) Identify the first load case
    let first_load_case_id: u32 = match fers_data.load_cases.first().map(|lc| lc.id) {
        Some(id) => id,
        None => return Err("No load cases found in the input data.".to_string()),
    };

    // 3) Perform the structural analysis
    let results = fers_data
        .solve_for_load_case(first_load_case_id)
        .map_err(|e| format!(
            "Error during analysis for Load Case {}: {}",
            first_load_case_id, e
        ))?;

    // Serialize `Results` to JSON
    serde_json::to_string(&results)
        .map_err(|e| format!("Failed to serialize results: {}", e))
    }


/// A small helper for printing displacement or reaction vectors more nicely.
#[allow(dead_code)]
fn print_readable_vector(vector: &DMatrix<f64>, label: &str) {
    let dof_labels = ["UX", "UY", "UZ", "RX", "RY", "RZ"];
    println!("{}:", label);

    // We assume 6 DOFs per node
    let num_nodes = vector.nrows() / 6;
    for node_index in 0..num_nodes {
        println!("  Node {}:", node_index + 1);
        for dof_index in 0..6 {
            let value = vector[(node_index * 6 + dof_index, 0)];
            println!("    {:<3}: {:10.4}", dof_labels[dof_index], value);
        }
    }
}

/// Convenience function for reading a file and passing its contents to `calculate_from_json_internal`.
pub fn calculate_from_file_internal(path: &str) -> Result<String, String> {
    let file_content = match fs::read_to_string(path) {
        Ok(content) => content,
        Err(e) => return Err(format!("Failed to read JSON file: {}", e)),
    };

    calculate_from_json_internal(&file_content)
}

pub fn load_fers_from_file<P: AsRef<Path>>(path: P) -> Result<FERS, io::Error> {
    let s = fs::read_to_string(path)?;
    let fers: FERS = serde_json::from_str(&s)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
    Ok(fers)
}