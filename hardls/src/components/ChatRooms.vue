<template lang="html">
    <div class="col-12">
        <b-row>
            <b-col cols="12" md="4" class="form-elegant scrollbar bg-dark p-0 m-0" style="max-height: 80vh;" >
                <b-list-group-item v-for="room in rooms" v-bind:key="room.id">
                    <button @click="go_to_room(room.room_name)">{{ room.room_name }}</button>
                </b-list-group-item>
            </b-col>
            <b-col cols="12" md="8" class="bg-secondary text-light m-0 p-0">
                <div class="form-elegant scrollbar" id="messages_area" style="height: 80vh;"></div>
                <b-form-input v-model="text" id="input-1" type="email" required placeholder="Enter email"></b-form-input>
                <b-button @click="send()" class="col-12" type="button">Send</b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12">
                <b-list-group-item >
                    <p>{{ newMess }}</p>
                </b-list-group-item>
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
            token: '56d66435e28dc026598d684904bcdac48ff4b4a1',
            isAuth: false,
            text: '',
            connected: false,
            newMess: [],
        };
    },
    mounted () {
        const axios = require('axios');//localStorage.getItem('token');
        axios.get(
          'http://127.0.0.1:8000/chat/rooms/',
          {headers: { Authorization: "Token " + this.token }}
        ).then(response => (
          this.rooms = response.data,
          this.isAuth = true,
          console.log(this.rooms)
        )).catch(error => (
            console.log(this.error)
        ));
    },
    methods: {
        go_to_room (chatroom) {
            this.chatSocket = new WebSocket(
                'ws://'+ '127.0.0.1:8000' + '/ws/chat/' + chatroom + '/?token=' + this.token
            );
            this.chatSocket.onopen = function(e) {
                //console.log(e.data);
            };
            this.chatSocket.onmessage = function(e) {
                this.newMess.push(e.data);
                const data = JSON.parse(e.data);
                if(data.message){
                    console.log(this.newMess);
                    $('#messages_area').append('<div class="col-11 bg-dark rounded text-light py-2 my-3 mx-auto">' + data.message + ' - ' + data.user + '</div>');
                }
            }
        },
        send () {
            this.chatSocket.send(JSON.stringify({
                'message': this.text,
            }));
        }
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
