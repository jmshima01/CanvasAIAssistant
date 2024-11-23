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

 
}}
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