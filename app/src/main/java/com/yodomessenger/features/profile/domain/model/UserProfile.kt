package com.yodomessenger.features.profile.domain.model

import com.google.firebase.firestore.ServerTimestamp
import java.util.Date

data class UserProfile(
    val uid: String = "",
    val nickname: String = "",
    val username: String = "",
    val bio: String = "",               // Описание "о себе"
    val dateOfBirth: String = "",       // Формат: YYYY-MM-DD
    val notes: String = "",             // Приватные заметки (видны только владельцу)
    @ServerTimestamp
    val createdAt: Date? = null,
    val privacySettings: PrivacySettings = PrivacySettings()
)

data class PrivacySettings(
    val showLastSeen: Boolean = true,
    val showBio: Boolean = true,
    val showDob: Boolean = false,
    val autoHideKeyboardAfterSend: Boolean = true // Связано с Пунктом 7
)
