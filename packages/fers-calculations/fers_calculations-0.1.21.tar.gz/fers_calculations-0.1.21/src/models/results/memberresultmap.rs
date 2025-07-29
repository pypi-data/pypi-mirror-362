use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct MemberResultMap {
    pub data: HashMap<String, HashMap<String, f64>>, 
}