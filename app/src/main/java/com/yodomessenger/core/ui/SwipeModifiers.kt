package com.yodomessenger.core.ui

import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput

/**
 * Свайп влево для ответа на сообщение.
 */
fun Modifier.swipeToReply(
    threshold: Float = 150f,
    onReply: () -> Unit
): Modifier = this.pointerInput(Unit) {
    var totalDrag = 0f
    detectHorizontalDragGestures(
        onDragEnd = {
            if (totalDrag < -threshold) {
                onReply()
            }
            totalDrag = 0f // Сброс после завершения жеста
        },
        onHorizontalDrag = { _, dragAmount ->
            totalDrag += dragAmount
        }
    )
}

/**
 * Свайп слева направо для возврата назад (Edge Swipe).
 */
fun Modifier.swipeToGoBack(
    threshold: Float = 100f,
    onGoBack: () -> Unit
): Modifier = this.pointerInput(Unit) {
    var totalDrag = 0f
    detectHorizontalDragGestures(
        onDragEnd = {
            if (totalDrag > threshold) {
                onGoBack()
            }
            totalDrag = 0f // Сброс после завершения жеста
        },
        onHorizontalDrag = { _, dragAmount ->
            totalDrag += dragAmount
        }
    )
}
