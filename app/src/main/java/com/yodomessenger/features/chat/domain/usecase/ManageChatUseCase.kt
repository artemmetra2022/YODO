package com.yodomessenger.features.chat.domain.usecase

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
