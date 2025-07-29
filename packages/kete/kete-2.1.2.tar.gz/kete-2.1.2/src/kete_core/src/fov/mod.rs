//! # Field of View
//! On-Sky field of view checks.
mod fov_like;
mod generic;
mod neos;
mod patches;
mod ptf;
mod spherex;
mod wise;
mod ztf;

pub use self::fov_like::FovLike;
pub use self::generic::{GenericCone, GenericRectangle, OmniDirectional};
pub use self::neos::{NeosCmos, NeosVisit};
pub use self::patches::{Contains, OnSkyRectangle, SkyPatch, SphericalCone, SphericalPolygon};
pub use self::ptf::{PTFFilter, PtfCcd, PtfField};
pub use self::spherex::{SpherexCmos, SpherexField};
pub use self::wise::WiseCmos;
pub use self::ztf::{ZtfCcdQuad, ZtfField};

use serde::{Deserialize, Serialize};

use crate::{frames::Vector, prelude::*};

/// Allowed FOV objects, either contiguous or joint.
/// Many of these exist solely to carry additional metadata.
#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum FOV {
    /// Omni-Directional FOV.
    OmniDirectional(OmniDirectional),

    /// Generic cone FOV without any additional metadata.
    GenericCone(GenericCone),

    /// Generic rectangle FOV without any additional metadata.
    GenericRectangle(GenericRectangle),

    /// WISE or NEOWISE FOV.
    Wise(WiseCmos),

    /// NEOS single cmos FOV.
    NeosCmos(NeosCmos),

    /// NEOS Visit.
    NeosVisit(NeosVisit),

    /// ZTF Single Quad of single CCD FOV.
    ZtfCcdQuad(ZtfCcdQuad),

    /// Full ZTF field of up to 64 individual files.
    ZtfField(ZtfField),

    /// Single PTF CCD image.
    PtfCcd(PtfCcd),

    /// Full PTF field of multiple ccd images.
    PtfField(PtfField),

    /// Spherex CMOS
    SpherexCmos(SpherexCmos),

    /// Spherex Field, containing up to 6 CMOS frames.
    SpherexField(SpherexField),
}

impl FOV {
    /// Check if a collection of states are visible to this FOV using orbital propagation
    pub fn check_visible(
        self,
        states: &[State<Equatorial>],
        dt_limit: f64,
        include_asteroids: bool,
    ) -> Vec<Option<SimultaneousStates>> {
        match self {
            Self::Wise(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::NeosCmos(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::ZtfCcdQuad(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::GenericCone(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::GenericRectangle(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::ZtfField(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::NeosVisit(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::OmniDirectional(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::PtfCcd(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::PtfField(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::SpherexCmos(fov) => fov.check_visible(states, dt_limit, include_asteroids),
            Self::SpherexField(fov) => fov.check_visible(states, dt_limit, include_asteroids),
        }
    }

    /// Observer position in this FOV
    pub fn observer(&self) -> &State<Equatorial> {
        match self {
            Self::Wise(fov) => fov.observer(),
            Self::NeosCmos(fov) => fov.observer(),
            Self::ZtfCcdQuad(fov) => fov.observer(),
            Self::GenericCone(fov) => fov.observer(),
            Self::GenericRectangle(fov) => fov.observer(),
            Self::ZtfField(fov) => fov.observer(),
            Self::NeosVisit(fov) => fov.observer(),
            Self::OmniDirectional(fov) => fov.observer(),
            Self::PtfCcd(fov) => fov.observer(),
            Self::PtfField(fov) => fov.observer(),
            Self::SpherexCmos(fov) => fov.observer(),
            Self::SpherexField(fov) => fov.observer(),
        }
    }

    /// Check if any loaded SPK objects are visible to this FOV
    pub fn check_spks(&self, obj_ids: &[i32]) -> Vec<Option<SimultaneousStates>> {
        match self {
            Self::Wise(fov) => fov.check_spks(obj_ids),
            Self::NeosCmos(fov) => fov.check_spks(obj_ids),
            Self::ZtfCcdQuad(fov) => fov.check_spks(obj_ids),
            Self::GenericCone(fov) => fov.check_spks(obj_ids),
            Self::GenericRectangle(fov) => fov.check_spks(obj_ids),
            Self::ZtfField(fov) => fov.check_spks(obj_ids),
            Self::NeosVisit(fov) => fov.check_spks(obj_ids),
            Self::OmniDirectional(fov) => fov.check_spks(obj_ids),
            Self::PtfCcd(fov) => fov.check_spks(obj_ids),
            Self::PtfField(fov) => fov.check_spks(obj_ids),
            Self::SpherexCmos(fov) => fov.check_spks(obj_ids),
            Self::SpherexField(fov) => fov.check_spks(obj_ids),
        }
    }

    /// Check if static sources are visible in this FOV.
    pub fn check_statics(&self, pos: &[Vector<Equatorial>]) -> Vec<Option<(Vec<usize>, Self)>> {
        match self {
            Self::Wise(fov) => fov.check_statics(pos),
            Self::NeosCmos(fov) => fov.check_statics(pos),
            Self::ZtfCcdQuad(fov) => fov.check_statics(pos),
            Self::GenericCone(fov) => fov.check_statics(pos),
            Self::GenericRectangle(fov) => fov.check_statics(pos),
            Self::ZtfField(fov) => fov.check_statics(pos),
            Self::NeosVisit(fov) => fov.check_statics(pos),
            Self::OmniDirectional(fov) => fov.check_statics(pos),
            Self::PtfCcd(fov) => fov.check_statics(pos),
            Self::PtfField(fov) => fov.check_statics(pos),
            Self::SpherexCmos(fov) => fov.check_statics(pos),
            Self::SpherexField(fov) => fov.check_statics(pos),
        }
    }
}
