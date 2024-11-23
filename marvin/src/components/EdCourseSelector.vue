// EdCourseSelector.vue
<template>
  <v-card class="pa-4" elevation="2">
    <v-form @submit.prevent="submitCourse">
      <div class="d-flex flex-column">
        <!-- Loading state for courses -->
        <div v-if="loadingCourses" class="d-flex justify-center ma-4">
          <v-progress-circular indeterminate></v-progress-circular>
        </div>
        
        <!-- Error message -->
        <v-alert
          v-if="error"
          type="error"
          class="mb-4"
          closable
          @click:close="error = null"
        >
          {{ error }}
        </v-alert>

        <!-- Success message -->
        <v-alert
          v-if="successMessage"
          type="success"
          class="mb-4"
          closable
          @click:close="successMessage = null"
        >
          {{ successMessage }}
        </v-alert>

        <!-- Course Selection -->
        <v-select
          v-model="selectedCourse"
          :items="courseItems"
          label="Select Course"
          :loading="loadingCourses"
          :disabled="loadingCourses || loading"
          item-title="title"
          item-value="id"
          return-object
          class="mb-4"
        >
          <template v-slot:no-data>
            <div class="pa-2">No courses available</div>
          </template>
        </v-select>

        <!-- Submit Button -->
        <v-btn
          color="primary"
          type="submit"
          :disabled="!selectedCourse || loading"
          :loading="loading"
          class="align-self-end"
        >
          Set Course
        </v-btn>
      </div>
    </v-form>
  </v-card>
</template>

<script>
export default {
  name: 'EdCourseSelector',
  emits: ['course-selected'],
  data() {
    return {
      courseItems: [],
      selectedCourse: null,
      loading: false,
      loadingCourses: false,
      error: null,
      successMessage: null
    }
  },
  created() {
    this.fetchCourses()
  },
  methods: {
    async fetchCourses() {
      this.loadingCourses = true
      this.error = null
      
      try {
        const response = await fetch('http://127.0.0.1:8000/ed/list-courses', {
          method: 'GET',
          headers: {
            'accept': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch courses')
        }

        const data = await response.json()
        
        // Transform the data into the format needed for v-select
        this.courseItems = Object.entries(data).map(([id, title]) => ({
          id: parseInt(id), // Ensure ID is a number
          title: title
        }))
      } catch (error) {
        console.error('Error fetching courses:', error)
        this.error = 'Failed to load courses. Please try again later.'
      } finally {
        this.loadingCourses = false
      }
    },

    
    async submitCourse() {
      if (!this.selectedCourse) return
      
      this.loading = true
      this.error = null
      this.successMessage = null

      try {
        // Fixed: Send course_id as URL parameter instead of body
        const response = await fetch(`http://127.0.0.1:8000/ed/select-course?course_id=${this.selectedCourse.id}`, {
          method: 'POST',
          headers: {
            'accept': 'application/json'
          },
          // No body needed
          body: ''
        })

        if (!response.ok) {
          throw new Error('Failed to set course')
        }

        // If successful
        this.successMessage = `Successfully set course: ${this.selectedCourse.title}`
        this.$emit('course-selected', this.selectedCourse)
        
      } catch (error) {
        console.error('Error setting course:', error)
        this.error = 'Failed to set course. Please try again.'
      } finally {
        this.loading = false
      }
    },

    // Refresh courses list
    refreshCourses() {
      this.fetchCourses()
    }
  }
}
</script>