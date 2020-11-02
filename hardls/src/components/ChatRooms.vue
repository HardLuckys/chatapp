<template lang="html">
    <div class="col-12 p-0 m-0">
        <b-row class="p-0 m-0">
            <h3>Rooms</h3>
            <b-col v-if="room == ''" cols="12" class="form-elegant scrollbar bg-secondary p-0 m-0" style="max-height: 80vh;" >
                <b-row class="p-3 m-0 d-flex justify-content-center">
                      <b-card v-for="room in rooms" bg-variant="dark" text-variant="white" header="Secondary" class="text-center col-3 p-1 mx-2 my-3">
                        <b-card-text><a @click="go_to_room(room.room_name)" class="text-light">{{ room.room_name }}</a></b-card-text>
                      </b-card>
                </b-row>

            </b-col>
            <b-col v-else cols="12" class="bg-secondary text-light m-0 p-0">
                <h3>Chat-room: {{ room }}</h3>
                <div class="form-elegant scrollbar m-0 p-0" id="messages_area" style="height: 80vh;">
                    <div v-for="mess in newMess" class="col-11 bg-dark rounded text-light py-2 my-3 mx-auto">{{ mess.message }} От {{ mess.user }} Дата: {{ mess.date }}</div>
                </div>
                <b-row class="bg-dark m-0 p-0">
                    <b-col cols="8" class="p-0 m-1 mx-auto">
                        <b-form-input v-model="text" id="input-message" type="text" required placeholder="Enter text"></b-form-input>
                    </b-col>
                    <b-col cols="3" class="p-0 m-1 mx-auto">
                        <b-button @click="send()" variant="success" class="col-12" type="button">Send</b-button>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>

<script>
export default {
    name: 'ChatRooms',
    data () {
        return {
            rooms: [],
            chatSocket: null,
            token: '',
            isAuth: false,
            text: '',
            connected: false,
            newMess: [],
            room: '',
            in_room: false,
            user: 'hardls' //проверка пользователя по токену
      };
    },
    mounted () {
        const axios = require('axios');
        this.token = localStorage.getItem('token');
        axios.get(
          'http://127.0.0.1:8000/chat/rooms/',
          {headers: { Authorization: "Token " + this.token }}
        ).then(response => (
          this.rooms = response.data
        )).catch(error => (
            console.log(this.error)
        ));
    },
    methods: {
        go_to_room (chatroom) {
            this.room = chatroom;
            this.newMess = [];
            this.chatSocket = null;
            this.chatSocket = new WebSocket(
                'ws://'+ '127.0.0.1:8000' + '/ws/chat/' + chatroom + '/?token=' + this.token
            );
            this.chatSocket.onopen = function(e) {
            };
            this.chatSocket.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if(data.connected_user && data.connected_user != this.user)
                {
                    alert(data.connected_user + ' присоединился');
                } else if(data.disconnected_user) {
                    alert(data.disconnected_user + ' отсоединился');
                }
                if(data.message){
                    this.newMess.push(data);
                }
            };
            this.chatSocket.onclose = function(e) {
                console.log(e.data);
            };
        },
        send () {
            this.chatSocket.send(JSON.stringify({
                'message': this.text,
            }));
            this.text = '';
        },
    }
}



</script>

<style lang="css" scoped>
    .form-elegant{
        position: relative;
        overflow-y: scroll;
    }

    .scrollbar-light-blue::-webkit-scrollbar-track {
        -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1);
        background-color: #F5F5F5;
        border-radius: 10px;
    }
    .scrollbar-light-blue::-webkit-scrollbar {
        width: 12px;
        background-color: #F5F5F5;
    }
    .scrollbar-light-blue::-webkit-scrollbar-thumb {
        border-radius: 10px;
        -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.1);
        background-color: #82B1FF;
    }
</style>
