package com.yodomessenger.core.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

enum class YodoThemeType(val seedColor: Long, val displayName: String) {
    SYSTEM(0xFF000000, "Как в системе"),
    TELEGRAM_BLUE(0xFF2AABEE, "Telegram Blue"),
    FOREST_GREEN(0xFF4CAF50, "Forest Green"),
    SUNSET_ORANGE(0xFFFF9800, "Sunset Orange"),
    ROYAL_PURPLE(0xFF9C27B0, "Royal Purple"),
    CRIMSON_RED(0xFFE53935, "Crimson Red")
}

@Composable
fun getYodoColorScheme(themeType: YodoThemeType, darkTheme: Boolean): ColorScheme {
    val context = LocalContext.current
    return when (themeType) {
        YodoThemeType.SYSTEM -> {
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        else -> {
            val seed = Color(themeType.seedColor)
            if (darkTheme) {
                darkColorScheme(
                    primary = seed,
                    secondaryContainer = seed.copy(alpha = 0.2f),
                    onSecondaryContainer = seed.copy(alpha = 0.9f)
                )
            } else {
                lightColorScheme(
                    primary = seed,
                    secondaryContainer = seed.copy(alpha = 0.15f),
                    onSecondaryContainer = seed
                )
            }
        }
    }
}
