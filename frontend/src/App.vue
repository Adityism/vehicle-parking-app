&lt;template>
  <router-view></router-view>
</template>

<script>
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import 'bootstrap/dist/css/bootstrap.min.css'

export default {
  name: 'App',
  setup() {
    const store = useStore()

    onMounted(async () => {
      if (store.state.token) {
        try {
          await store.dispatch('getCurrentUser')
        } catch (error) {
          console.error('Failed to restore session:', error)
        }
      }
    })
  }
}
</script>

<style>
body {
  margin: 0;
  background-color: #f8f9fa;
}
</style>
</style>
