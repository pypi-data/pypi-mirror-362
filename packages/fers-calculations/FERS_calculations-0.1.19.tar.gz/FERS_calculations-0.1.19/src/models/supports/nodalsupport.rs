use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use std::collections::HashMap;


#[derive(Serialize, Deserialize, ToSchema
, Debug)]
pub struct NodalSupport {
    pub id: u32,
    pub classification: Option<String>,
    pub displacement_conditions: HashMap<String, String>,
    pub rotation_conditions: HashMap<String, String>,
}
