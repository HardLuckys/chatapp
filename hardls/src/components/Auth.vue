<template>
  <div v-if="authorized" class="col-12" style="height: 100vh; background: #000;">
    <div class="row align-items-center col-md-6 mx-3 mx-auto" style="height: 100vh;">
      <form class="row align-items-center col-12" style="height: 50vh;">
        <div class="col-12 text-center">
          <h3 class="text-light">Авторизация</h3>
          <p v-if="errored" class="text-danger col-12 text-center">Ошибка. Данные введены не верно.</p>
          <input v-model="username" @input="goLogin()" :class="{'is-invalid': errored}" type="username" min="3" max="12" class="form-control col-12 my-5" placeholder="username">
          <input v-model="password" @input="goLogin()" :class="{'is-invalid': errored}" type="password" class="form-control col-12 my-5" placeholder="Password">
          <small class="text-muted text-center">Если вы ввели данные верно вас авторизует.</small>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Auth',
  data () {
    return {
      username: '',
      password: '',
      errored: false,
      authorized: false
    }
  },
  mounted () {

    if (this.authorized = true && localStorage.getItem('token') !== null){
      this.$router.push({name: 'ChatRooms'})
    } else {
      this.authorized = true
    }
  },
  methods: {
    ChatRooms() {
      this.$router.push({name: 'ChatRooms'})
    },
    goLogin() {
      if (this.username.length > 2 && this.password.length > 0 ) {
        const axios = require('axios');
        axios.post(
          'http://127.0.0.1:8000/api-token-auth/',
          {
            username: this.username,
            password: this.password
          }
        ).then(response => (
          this.ChatRooms(),
          localStorage.setItem('token', response.data['auth_token']),
          this.authorized = true,
          console.log(response.data)
        )).catch(error =>
          this.errored = true,
        )
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
