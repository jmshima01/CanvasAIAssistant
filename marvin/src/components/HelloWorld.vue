<template>
  <!-- API Keys Section -->
  <v-container>
    <v-row>
      <v-col cols="12" sm="8" md="6">
        <v-form @submit.prevent="submitOpenAI">
          <v-text-field
            v-model="openaiKey"
            label="OpenAI Token"
            :error-messages="openaiError"
            :loading="openaiLoading"
            type="password"
            clearable
            placeholder="Enter your OpenAI API key"
          ></v-text-field>
         
          <v-btn
            type="submit"
            color="primary"
            :loading="openaiLoading"
          >
            {{ openaiSuccess ? 'Connected' : 'Submit OpenAI Token' }}
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
  
  <v-container>
    <v-row>
      <v-col cols="12" sm="8" md="6">
        <v-form @submit.prevent="submitCanvas">
          <v-text-field
            v-model="canvasKey"
            label="Canvas Token"
            :error-messages="canvasError"
            :loading="canvasLoading"
            type="password"
            clearable
            placeholder="Enter your Canvas API key"
          ></v-text-field>
         
          <v-btn
            type="submit"
            color="primary"
            :loading="canvasLoading"
          >
            {{ canvasSuccess ? 'Connected' : 'Submit Canvas Token' }}
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>

  <v-container>
    <v-row>
      <v-col cols="12" sm="8" md="6">
        <v-form @submit.prevent="submitEdStem">
          <v-text-field
            v-model="edStemKey"
            label="EdStem Token"
            :error-messages="edStemError"
            :loading="edStemLoading"
            type="password"
            clearable
            placeholder="Enter your EdStem API key"
          ></v-text-field>
         
          <v-btn
            type="submit"
            color="primary"
            :loading="edStemLoading"
          >
            {{ edStemSuccess ? 'Connected' : 'Submit EdStem Token' }}
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>

  <!-- Chat Section - Now always visible -->
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-card class="mb-6" height="400" elevation="2">
          <v-card-text class="chat-container overflow-y-auto">
            <template v-for="(message, index) in messages" :key="index">
              <!-- User Message -->
              <div v-if="message.type === 'user'" class="d-flex justify-end mb-4">
                <v-card color="primary" class="rounded-lg" max-width="70%">
                  <v-card-text class="text-white">
                    {{ message.content }}
                  </v-card-text>
                </v-card>
              </div>

              <!-- Assistant Message -->
              <div v-else class="d-flex justify-start mb-4">
                <v-card class="rounded-lg" max-width="70%">
                  <v-card-text>
                    {{ message.content }}
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
        <v-form @submit.prevent="sendMessage">
          <div class="d-flex">
            <v-text-field
              v-model="userInput"
              placeholder="Type your message..."
              :disabled="chatLoading"
              @keyup.enter="sendMessage"
              hide-details
              class="mr-2"
            ></v-text-field>
            <v-btn
              color="primary"
              type="submit"
              :loading="chatLoading"
              :disabled="!userInput.trim()"
            >
              Send
            </v-btn>
          </div>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      // API Keys data
      openaiKey: '',
      canvasKey: '',
      edStemKey: '',
      openaiLoading: false,
      canvasLoading: false,
      edStemLoading: false,
      openaiError: '',
      canvasError: '',
      edStemError: '',
      openaiSuccess: false,
      canvasSuccess: false,
      edStemSuccess: false,

      // Chat data
      messages: [],
      userInput: '',
      chatLoading: false,
    }
  },

  methods: {
    async submitOpenAI() {
      this.openaiLoading = true;
      this.openaiError = '';
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/openai?api_key=${encodeURIComponent(this.openaiKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
       
        if (!response.ok) {
          throw new Error('Login failed');
        }
       
        const data = await response.json();
        console.log('OpenAI login successful:', data);
        this.openaiSuccess = true;
        localStorage.setItem('openaiToken', data.token);
       
      } catch (error) {
        console.error('Error:', error);
        this.openaiError = 'Login failed. Please check your OpenAI token and try again.';
      } finally {
        this.openaiLoading = false;
      }
    },

    async submitCanvas() {
      this.canvasLoading = true;
      this.canvasError = '';
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/canvas?canvas_token=${encodeURIComponent(this.canvasKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
       
        if (!response.ok) {
          throw new Error('Login failed');
        }
       
        const data = await response.json();
        console.log('Canvas login successful:', data);
        this.canvasSuccess = true;
        localStorage.setItem('canvasToken', data.token);
       
      } catch (error) {
        console.error('Error:', error);
        this.canvasError = 'Login failed. Please check your Canvas token and try again.';
      } finally {
        this.canvasLoading = false;
      }
    },

    async submitEdStem() {
      this.edStemLoading = true;
      this.edStemError = '';
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/edstem?ed_token=${encodeURIComponent(this.edStemKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
       
        if (!response.ok) {
          throw new Error('Login failed');
        }
       
        const data = await response.json();
        console.log('EdStem login successful:', data);
        this.edStemSuccess = true;
        localStorage.setItem('edStemToken', data.token);
       
      } catch (error) {
        console.error('Error:', error);
        this.edStemError = 'Login failed. Please check your EdStem token and try again.';
      } finally {
        this.edStemLoading = false;
      }
    },

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
        const response = await fetch(`http://127.0.0.1:8000/ask/canvas?question=${encodeURIComponent(userMessage)}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('API request failed');
        }

        // Get response as text since it returns a string
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
  },
}
</script>

<style scoped>
.chat-container {
  height: 400px;
  overflow-y: auto;
  padding: 20px;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>