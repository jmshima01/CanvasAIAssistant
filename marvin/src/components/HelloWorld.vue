<template>
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
            :disabled="!openaiKey"
          >
            Submit OpenAI Token
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
            :disabled="!canvasKey"
          >
            Submit Canvas Token
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
            :disabled="!edStemKey"
          >
            Submit EdStem Token
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
      openaiKey: '',
      canvasKey: '',
      edStemKey: '',
      openaiLoading: false,
      canvasLoading: false,
      edStemLoading: false,
      openaiError: '',
      canvasError: '',
      edStemError: '',
    }
  },
  methods: {
    async submitOpenAI() {
      this.openaiLoading = true
      this.openaiError = ''
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/openai?api_key=${encodeURIComponent(this.openaiKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
       
        if (!response.ok) {
          throw new Error('Login failed')
        }
       
        const data = await response.json()
        console.log('OpenAI login successful:', data)
        this.openaiKey = '' // Clear the input after success
       
        // Handle successful login here (e.g., store token, redirect, etc.)
       
      } catch (error) {
        console.error('Error:', error)
        this.openaiError = 'Login failed. Please check your OpenAI token and try again.'
      } finally {
        this.openaiLoading = false
      }
    },

    async submitCanvas() {
      this.canvasLoading = true
      this.canvasError = ''
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/canvas?api_key=${encodeURIComponent(this.canvasKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
       
        if (!response.ok) {
          throw new Error('Login failed')
        }
       
        const data = await response.json()
        console.log('Canvas login successful:', data)
        this.canvasKey = '' // Clear the input after success
       
        // Handle successful login here (e.g., store token, redirect, etc.)
       
      } catch (error) {
        console.error('Error:', error)
        this.canvasError = 'Login failed. Please check your Canvas token and try again.'
      } finally {
        this.canvasLoading = false
      }
    },

    async submitEdStem() {
      this.edStemLoading = true
      this.edStemError = ''
     
      try {
        const response = await fetch(`http://127.0.0.1:8000/login/edstem?api_key=${encodeURIComponent(this.edStemKey)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
       
        if (!response.ok) {
          throw new Error('Login failed')
        }
       
        const data = await response.json()
        console.log('EdStem login successful:', data)
        this.edStemKey = '' // Clear the input after success
       
        // Handle successful login here (e.g., store token, redirect, etc.)
       
      } catch (error) {
        console.error('Error:', error)
        this.edStemError = 'Login failed. Please check your EdStem token and try again.'
      } finally {
        this.edStemLoading = false
      }
    },
  },
}
</script>