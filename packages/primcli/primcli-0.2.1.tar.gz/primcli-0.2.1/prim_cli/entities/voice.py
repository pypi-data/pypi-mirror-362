from .base import BaseEntity, BaseRepository


class Voice(BaseEntity):
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        organization_id: str = None,
        name: str = None,
        description: str = None,
        voice_id: str = None,
        created_at: str = None,
        updated_at: str = None,
        deleted_at: str = None,
        base_voice_id: str = None,
        is_base: bool = None,
        is_cloned: bool = None,
        is_community: bool = None,
        is_flash_enabled: bool = None,
        is_owner: bool = None,
        public: bool = None,
        verified: bool = None,
        # Audio URLs
        sample_url: str = None,
        preview_url: str = None,
        normalized_sample_url: str = None,
        normalized_preview_url: str = None,
        preferred_sample_url: str = None,
        preferred_preview_url: str = None,
        full_original_sample_url: str = None,
        # User-related fields
        user_description: str = None,
        user_age_description: str = None,
        user_gender_description: str = None,
        user_image_upload: str = None,
        user_image_upload_thumbnail: str = None,
        # Voice characteristics
        jitter: str = None,
        jitter_mean_auto_description: str = None,
        meanf0pitch: str = None,
        meanf0pitch_auto_description: str = None,
        onset_strength_mean: str = None,
        onset_strength_mean_auto_description: str = None,
        spectral_centroid_mean: str = None,
        spectral_centroid_mean_auto_description: str = None,
        spectral_contrast_mean: str = None,
        spectral_contrast_mean_auto_description: str = None,
        spectral_flatness_mean: str = None,
        spectral_flatness_mean_auto_description: str = None,
        zero_crossing_rate_mean: str = None,
        zero_crossing_rate_mean_auto_description: str = None,
        # Metadata
        tags: str = None,
    ):
        self.id = id
        self.user_id = user_id
        self.organization_id = organization_id
        self.name = name
        self.description = description
        self.voice_id = voice_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at or None
        
        # Additional fields
        self.base_voice_id = base_voice_id
        self.is_base = is_base
        self.is_cloned = is_cloned
        self.is_community = is_community
        self.is_flash_enabled = is_flash_enabled
        self.is_owner = is_owner
        self.public = public
        self.verified = verified
        
        # Audio URLs
        self.sample_url = sample_url
        self.preview_url = preview_url
        self.normalized_sample_url = normalized_sample_url
        self.normalized_preview_url = normalized_preview_url
        self.preferred_sample_url = preferred_sample_url
        self.preferred_preview_url = preferred_preview_url
        self.full_original_sample_url = full_original_sample_url
        
        # User-related fields
        self.user_description = user_description
        self.user_age_description = user_age_description
        self.user_gender_description = user_gender_description
        self.user_image_upload = user_image_upload
        self.user_image_upload_thumbnail = user_image_upload_thumbnail
        
        # Voice characteristics
        self.jitter = jitter
        self.jitter_mean_auto_description = jitter_mean_auto_description
        self.meanf0pitch = meanf0pitch
        self.meanf0pitch_auto_description = meanf0pitch_auto_description
        self.onset_strength_mean = onset_strength_mean
        self.onset_strength_mean_auto_description = onset_strength_mean_auto_description
        self.spectral_centroid_mean = spectral_centroid_mean
        self.spectral_centroid_mean_auto_description = spectral_centroid_mean_auto_description
        self.spectral_contrast_mean = spectral_contrast_mean
        self.spectral_contrast_mean_auto_description = spectral_contrast_mean_auto_description
        self.spectral_flatness_mean = spectral_flatness_mean
        self.spectral_flatness_mean_auto_description = spectral_flatness_mean_auto_description
        self.zero_crossing_rate_mean = zero_crossing_rate_mean
        self.zero_crossing_rate_mean_auto_description = zero_crossing_rate_mean_auto_description
        
        # Metadata
        self.tags = tags


class VoiceRepository(BaseRepository[Voice]):
    def __init__(self):
        super().__init__("voice", f"/v1/voices", Voice)