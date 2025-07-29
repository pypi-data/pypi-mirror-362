use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::models::members::member::Member;

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct DistributedLoad {
    pub member: Member,
    pub load_case: u32,
    pub magnitude: f64,
    pub direction: (f64, f64, f64),
    pub start_pos: f64,
    pub end_pos: f64,
}
