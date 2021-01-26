import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

const vuexPersistence = new VuexPersistence({
    key: 'cards-against',
    storage: window.localStorage
});

export default new Vuex.Store({
    plugins: [vuexPersistence.plugin],
    state: {
        connected: false,
        error: '',
        errorField: '',
        message: '',
        username: '',
        userData: {},
        room: {},
        playedCards: [],
        winData: {},
    },
    mutations: {
        set_connected(state, payload) {
            state.connected = payload;
        },
        SOCKET_connect(state) {
            state.connected = true;
        },
        SOCKET_disconnect(state) {
            state.connected = false;
            console.error("Websocket disconnected");
        },
        SOCKET_message(state, message) {
            state.message = message;
        },
        SOCKET_error(state, message) {
            state.error = message.error;
            state.errorField = message.errorField;
            console.error(message);
        },
        error(state, message) {
            state.error = message.error;
            state.errorField = message.errorField;
        },
        SOCKET_join_room(state, data) {
            state.room = JSON.parse(data.room);
        },
        SOCKET_set_username(state, user) {
            state.username = user;
        },
        set_username(state, user) {
            state.username = user;
        },
        SOCKET_user_data(state, data) {
            state.userData = data;
        },
        SOCKET_played_cards(state, cards) {
            state.playedCards = cards;
        },
        SOCKET_round_over(state, data) {
            state.winData = data;
        }
    },
});