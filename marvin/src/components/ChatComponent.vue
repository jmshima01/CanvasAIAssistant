// ChatComponent.vue
<template>
  <v-container fluid class="fill-height pa-0">
    <v-row no-gutters class="fill-height">
      <v-col cols="12" class="d-flex flex-column">
        <!-- Chat Messages -->
        <v-card class="flex-grow-1 mb-4" elevation="2">
          <v-card-text class="chat-container d-flex flex-column" style="height: calc(100vh - 250px); overflow-y: auto;">
            <template v-for="(message, index) in messages" :key="index">
              <!-- User Message -->
              <div v-if="message.type === 'user'" class="d-flex justify-end mb-4">
                <v-card color="primary" class="rounded-lg" max-width="70%">
                  <v-card-text class="text-white message-text">
                    {{ message.content }}
                  </v-card-text>
                </v-card>
              </div>

              <!-- Assistant Message -->
              <div v-else class="d-flex justify-start mb-4">
                <v-card class="rounded-lg" max-width="70%">
                  <v-card-text class="message-text">
                    {{ message.content.split("\\n").join("\n").slice(1, -1).replace(/\\/g, "") }}
                  </v-card-text>
                </v-card>
              </div>
            </template>

            <!-- Loading indicator -->
            <div v-if="chatLoading" class="d-flex justify-start mb-4">
              <v-card class="rounded-lg" max-width="70%">
                <v-card-text>
                  <v-progress-circular indeterminate></v-progress-circular>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-card>

        <!-- Input Area -->
        <v-card class="pa-4" elevation="2">
          <v-form @submit.prevent="sendMessage">
            <div class="d-flex">
              <v-textarea
                v-model="userInput"
                :placeholder="placeholder"
                :disabled="chatLoading"
                @keydown.enter.prevent="sendMessage"
                hide-details
                rows="1"
                auto-grow
                class="mr-2"
              ></v-textarea>
              <v-btn
                color="primary"
                type="submit"
                :loading="chatLoading"
                :disabled="!userInput.trim()"
                height="40"
              >
                Send
              </v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ChatComponent',
  props: {
    apiEndpoint: {
      type: String,
      required: true
    },
    placeholder: {
      type: String,
      default: 'Type a message...'
    }
  },
  data() {
    return {
      messages: [],
      userInput: '',
      chatLoading: false,
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.chatLoading) return;

      this.messages.push({
        type: 'user',
        content: this.userInput.trim()
      });

      const userMessage = this.userInput.trim();
      this.userInput = '';
      this.chatLoading = true;

      try {
        const response = await fetch(`${this.apiEndpoint}?question=${encodeURIComponent(userMessage)}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('API request failed');
        }

        const data = await response.text();
        
        this.messages.push({
          type: 'assistant',
          content: data
        });

      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          type: 'assistant',
          content: 'Sorry, I encountered an error processing your request.'
        });
      } finally {
        this.chatLoading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    scrollToBottom() {
      const container = document.querySelector('.chat-container');
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  scroll-behavior: smooth;
}

.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.chat-container::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.chat-container {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>