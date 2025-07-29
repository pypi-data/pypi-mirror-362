use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema, Clone
, Debug)]
pub struct ReactionForce {
    pub support_id: u32,
    pub fx: f64,
    pub fy: f64,
    pub fz: f64,
    pub mx: f64,
    pub my: f64,
    pub mz: f64,
}
#[derive(Serialize, Deserialize, ToSchema, Clone
    , Debug)]
    pub struct MemberForce {
        pub member_id: u32,
        pub start_node_forces: NodeForces,
        pub end_node_forces: NodeForces,
    }
#[derive(Serialize, Deserialize, ToSchema, Clone
, Debug)]
pub struct NodeForces {
    pub fx: f64,
    pub fy: f64,
    pub fz: f64,
    pub mx: f64,
    pub my: f64,
    pub mz: f64,
} 