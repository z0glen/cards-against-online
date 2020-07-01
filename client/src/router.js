import Vue from 'vue';
import Router from 'vue-router';
import Home from "./components/Home";
import Game from './components/Game.vue';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home,
            meta: {
                title: 'Cards Against Online'
            }
        },
        {
            path: '/game/:code',
            name: 'Game',
            component: Game,
            props: true,
            meta: {
                title: 'Cards Against Online'
            }
        },
    ],
});
