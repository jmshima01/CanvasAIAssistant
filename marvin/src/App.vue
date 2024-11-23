<template>
  <v-app>
    <v-main>
      <v-card>
        <!-- Title Banner -->
        <v-toolbar density="compact">
          <v-toolbar-title class="text-h4 font-weight-bold white--text">
            MarvinAI
          </v-toolbar-title>
        </v-toolbar>

        <!-- Navigation tabs -->
        <v-tabs v-model="activeTab">
          <v-tab value="login">
            <v-icon start>mdi-cog</v-icon>
            Login
          </v-tab>
          
          <v-tab value="canvas">
            <v-icon start>mdi-account-school</v-icon>
            Canvas
          </v-tab>
          
          <v-tab value="ed">
            <v-icon start>mdi-forum</v-icon>
            Ed
          </v-tab>
        </v-tabs>

        <!-- Tab content -->
        <v-window v-model="activeTab">
          <!-- Login Tab Content -->
          <v-window-item value="login">
            <v-container>
              <HelloWorld/>
            </v-container>
          </v-window-item>

          <!-- Canvas Tab Content -->
          <v-window-item value="canvas">
            
            <v-container>
            <ChatComponent 
          api-endpoint="http://127.0.0.1:8000/ask/canvas"
          placeholder="Ask a question about Canvas..."
          /></v-container>
          
          </v-window-item>

          <!-- Ed Tab Content -->
          <v-window-item value="ed">
            <v-container>
              <!-- Add your ed content here -->
              <ChatComponent 
          api-endpoint="http://127.0.0.1:8000/ask/ed"
          placeholder="Ask a question about ed... Ask Marvin to post for you..."
          />
            </v-container>
            
          </v-window-item>
        </v-window>
      </v-card>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import ChatComponent from './components/ChatComponent.vue';
export default {
  name: 'NavigationTabs',
  data() {
    return {
      activeTab: 'login', // Default active tab
    }
  },
  methods: {
  }
}
</script>
