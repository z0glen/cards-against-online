import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        count: 0,
        connected: false,
        error: '',
        message: '',
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
        SOCKET_CONNECT(state) {
            state.connected = true;
        },
        SOCKET_DISCONNECT(state) {
            state.connected = false;
        },
        SOCKET_MESSAGE(state, message) {
            state.message = message;
        },
        SOCKET_HELLO_WORLD(state, message) {
            console.log(this.message);
            state.message = message;
        },
        SOCKET_ERROR(state, message) {
            state.error = message.error;
        },
    },
    actions: {
        reset_counter(context) {
            context.commit('set_counter', 0);
        }
    }
});