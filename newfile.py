#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического создания файлов проекта YodoMessenger
Запуск: python create_yodo_files.py
"""

import os
import sys

# Базовый путь проекта
BASE_PATH = "app/src/main/java/com/yodomessenger"

# Словарь с путями и содержимым файлов
FILES = {
    f"{BASE_PATH}/core/theme/AppTheme.kt": """package com.yodomessenger.core.theme

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
""",

    f"{BASE_PATH}/core/ui/SwipeModifiers.kt": """package com.yodomessenger.core.ui

import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput

/**
 * Свайп влево (dragAmount < 0) для ответа на сообщение.
 * @param threshold Порог срабатывания в пикселях (по умолчанию 150f)
 */
fun Modifier.swipeToReply(
    threshold: Float = 150f,
    onReply: () -> Unit
): Modifier = this.pointerInput(Unit) {
    detectHorizontalDragGestures(
        onDragEnd = { _, dragAmount ->
            if (dragAmount < -threshold) {
                onReply()
            }
        }
    ) { _, _ -> }
}

/**
 * Свайп слева направо (dragAmount > 0) для возврата на предыдущий экран.
 * Имитирует системный жест "Edge Swipe".
 */
fun Modifier.swipeToGoBack(
    threshold: Float = 100f,
    onGoBack: () -> Unit
): Modifier = this.pointerInput(Unit) {
    detectHorizontalDragGestures(
        onDragEnd = { _, dragAmount ->
            if (dragAmount > threshold) {
                onGoBack()
            }
        }
    ) { _, _ -> }
}
""",

    f"{BASE_PATH}/features/chat/ui/ImageViewerScreen.kt": """package com.yodomessenger.features.chat.ui

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Download
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.request.ImageRequest

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ImageViewerScreen(
    imageUrl: String,
    fileName: String = "yodo_image.jpg",
    onDismiss: () -> Unit
) {
    var scale by remember { mutableStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    val context = LocalContext.current

    Scaffold(
        containerColor = Color.Black,
        topBar = {
            TopAppBar(
                title = { Text("Просмотр", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, "Закрыть", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(onClick = { downloadImage(context, imageUrl, fileName) }) {
                        Icon(Icons.Default.Download, "Скачать", tint = Color.White)
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color.Black)
                .pointerInput(Unit) {
                    detectTransformGestures { _, pan, zoom, _ ->
                        scale = (scale * zoom).coerceIn(1f, 5f)
                        if (scale > 1f) {
                            offset = offset + pan
                        } else {
                            offset = Offset.Zero
                            scale = 1f
                        }
                    }
                },
            contentAlignment = Alignment.Center
        ) {
            AsyncImage(
                model = ImageRequest.Builder(context)
                    .data(imageUrl)
                    .crossfade(true)
                    .build(),
                contentDescription = "Full screen image",
                modifier = Modifier
                    .fillMaxSize()
                    .graphicsLayer(
                        scaleX = scale,
                        scaleY = scale,
                        translationX = offset.x,
                        translationY = offset.y
                    )
            )
        }
    }
}

private fun downloadImage(context: Context, imageUrl: String, fileName: String) {
    val request = DownloadManager.Request(Uri.parse(imageUrl)).apply {
        setTitle("Скачивание изображения")
        setDescription("YodoMessenger")
        setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        setDestinationInExternalPublicDir(Environment.DIRECTORY_PICTURES, "YodoMessenger/$fileName")
        setAllowedOverMetered(true)
    }
    val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
    downloadManager.enqueue(request)
    Toast.makeText(context, "Скачивание началось", Toast.LENGTH_SHORT).show()
}
""",

    f"{BASE_PATH}/features/chat/domain/usecase/ManageChatUseCase.kt": """package com.yodomessenger.features.chat.domain.usecase

import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import javax.inject.Inject

class ManageChatUseCase @Inject constructor(
    private val firestore: FirebaseFirestore
) {
    /**
     * Очищает историю сообщений в чате (soft-delete подход: удаляем документы сообщений).
     * Внимание: в продакшене лучше добавлять поле isDeleted = true, чтобы не терять метаданные.
     */
    suspend fun clearChatMessages(chatId: String) {
        val messagesRef = firestore.collection("chats").document(chatId).collection("messages")
        val snapshot = messagesRef.get().await()
        val batch = firestore.batch()
        
        for (document in snapshot.documents) {
            batch.delete(document.reference)
        }
        batch.commit().await()
        
        // Обновляем метаданные чата
        firestore.collection("chats").document(chatId).update(
            "lastMessageText", "История очищена",
            "lastMessageTimestamp", System.currentTimeMillis()
        ).await()
    }

    /**
     * Полностью удаляет чат (требует предварительной очистки сообщений для экономии квот).
     */
    suspend fun deleteChatCompletely(chatId: String) {
        clearChatMessages(chatId)
        firestore.collection("chats").document(chatId).delete().await()
    }
}
""",

    f"{BASE_PATH}/features/profile/domain/model/UserProfile.kt": """package com.yodomessenger.features.profile.domain.model

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
""",

    f"{BASE_PATH}/features/chat/ui/components/ChatInputField.kt": """package com.yodomessenger.features.chat.ui.components

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp

@Composable
fun ChatInputField(
    initialValue: String = "",
    autoHideKeyboard: Boolean,
    onSendMessage: (String) -> Unit
) {
    var text by remember { mutableStateOf(initialValue) }
    val keyboardController = LocalSoftwareKeyboardController.current

    val handleSend = {
        val trimmed = text.trim()
        if (trimmed.isNotEmpty()) {
            onSendMessage(trimmed)
            text = ""
            if (autoHideKeyboard) {
                keyboardController?.hide()
            }
        }
    }

    OutlinedTextField(
        value = text,
        onValueChange = { text = it },
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 4.dp),
        placeholder = { Text("Сообщение...") },
        shape = RoundedCornerShape(24.dp),
        keyboardOptions = KeyboardOptions.Default.copy(imeAction = ImeAction.Send),
        keyboardActions = KeyboardActions(onSend = { handleSend() }),
        trailingIcon = {
            IconButton(onClick = { handleSend() }) {
                Icon(Icons.Default.Send, contentDescription = "Отправить")
            }
        }
    )
}
""",

    f"{BASE_PATH}/core/ui/components/UserAvatar.kt": """package com.yodomessenger.core.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest

@Composable
fun UserAvatar(
    imageUrl: String?,
    userName: String,
    modifier: Modifier = Modifier,
    size: Dp = 48.dp,
    fallbackColor: Color = MaterialTheme.colorScheme.primary
) {
    val initials = userName.trim().take(2).uppercase()

    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .background(fallbackColor),
        contentAlignment = Alignment.Center
    ) {
        if (!imageUrl.isNullOrEmpty()) {
            AsyncImage(
                model = ImageRequest.Builder(LocalContext.current)
                    .data(imageUrl)
                    .crossfade(true)
                    .memoryCacheKey(imageUrl)
                    .diskCacheKey(imageUrl)
                    .build(),
                contentDescription = "Аватар $userName",
                modifier = Modifier.matchParentSize(),
                contentScale = ContentScale.Crop // Ключевой параметр для предотвращения искажений
            )
        }
        
        // Инициалы отображаются всегда, но если есть картинка, они будут под ней 
        // (или можно добавить проверку, чтобы показывать только при ошибке загрузки)
        if (imageUrl.isNullOrEmpty()) {
            Text(
                text = initials,
                color = MaterialTheme.colorScheme.onPrimary,
                fontWeight = FontWeight.Bold,
                fontSize = (size.value * 0.4).sp
            )
        }
    }
}
"""
}


def create_files():
    """Создает все файлы и папки проекта"""
    print("🚀 Начинаю создание файлов проекта YodoMessenger...\n")
    
    created_count = 0
    error_count = 0
    
    for file_path, content in FILES.items():
        try:
            # Создаем директории, если их нет
            directory = os.path.dirname(file_path)
            os.makedirs(directory, exist_ok=True)
            
            # Создаем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Создан: {file_path}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ Ошибка при создании {file_path}: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Итого создано файлов: {created_count}")
    if error_count > 0:
        print(f"⚠️  Ошибок: {error_count}")
    print(f"{'='*60}")
    
    if created_count == len(FILES):
        print("\n🎉 Все файлы успешно созданы!")
        print("\n📝 Следующие шаги:")
        print("1. Откройте проект в Android Studio")
        print("2. Синхронизируйте Gradle (File → Sync Project with Gradle Files)")
        print("3. Интегрируйте новые компоненты в существующий код")
        print("4. Обновите firestore.rules для безопасности")
    else:
        print("\n⚠️  Некоторые файлы не были созданы. Проверьте ошибки выше.")


if __name__ == "__main__":
    try:
        create_files()
    except KeyboardInterrupt:
        print("\n\n⚠️  Операция отменена пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)