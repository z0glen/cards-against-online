import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        count: 0,
        connected: false,
        error: '',
        message: '',
        user: '',
        room: {},
        playedCards: [],
    },
    getters: {
        doubleup(state) {
            return state.count * 2;
        },
    },
    mutations: {
        increment(state) {
            state.count++;
        },
        set_counter(state, newCount) {
            state.count = newCount;
        },
        set_connected(state, payload) {
            state.connected = payload;
        },
        SOCKET_connect(state) {
            state.connected = true;
        },
        SOCKET_DISCONNECT(state) {
            state.connected = false;
        },
        SOCKET_MESSAGE(state, message) {
            state.message = message;
        },
        SOCKET_HELLO_WORLD(state, message) {
            state.message = message;
        },
        SOCKET_error(state, message) {
            state.error = message.error;
        },
        SOCKET_join_room(state, data) {
            state.room = JSON.parse(data.room);
        },
        SOCKET_set_user(state, user) {
            state.user = user;
        },
        SOCKET_played_cards(state, cards) {
            state.playedCards = cards;
        }
    },
    actions: {
        reset_counter(context) {
            context.commit('set_counter', 0);
        },
    }
});