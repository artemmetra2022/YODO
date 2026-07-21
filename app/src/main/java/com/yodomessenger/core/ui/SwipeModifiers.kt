package com.yodomessenger.core.ui

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
