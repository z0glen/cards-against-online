import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Books from './components/Books.vue';
import Game from './components/Game.vue';
import Home from "./components/Home";
import Counter from "./components/Counter";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/ping',
            name: 'Ping',
            component: Ping,
        },
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/game/:code',
            name: 'Game',
            component: Game,
        },
        {
            path: '/books',
            name: 'Books',
            component: Books,
        },
        {
            path: '/counter',
            name: 'Counter',
            component: Counter,
        },
    ],
});
