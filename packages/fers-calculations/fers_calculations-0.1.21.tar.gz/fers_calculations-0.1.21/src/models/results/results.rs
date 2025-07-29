use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap};
use utoipa::ToSchema;
use crate::models::results::forces::{ReactionForce, MemberForce};
use crate::models::results::resultssummary::ResultsSummary;
use crate::models::results::memberresultmap::MemberResultMap;

use super::displacement::NodeDisplacement;

#[derive(Serialize, Deserialize, ToSchema, Debug, Clone)]
pub struct Results {
    pub name: String,
    pub result_type: String,
    pub displacement_nodes: BTreeMap<u32, NodeDisplacement>,
    pub reaction_forces: Vec<ReactionForce>,
    pub member_forces: Vec<MemberForce>,
    pub summary: ResultsSummary,
    pub member_minimums: Option<MemberResultMap>,
    pub member_maximums: Option<MemberResultMap>,
}


