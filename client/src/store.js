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
        count: 0,
        connected: false,
        error: '',
        errorField: '',
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
            state.errorField = message.errorField;
        },
        error(state, message) {
            state.error = message.error;
            state.errorField = message.errorField;
        },
        SOCKET_join_room(state, data) {
            state.room = JSON.parse(data.room);
        },
        SOCKET_set_user(state, user) {
            state.user = user;
        },
        set_user(state, user) {
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