<template>
    <div>
        <h1>Count: {{ count }} | Half: {{ halfCount }} | Double: {{ doubleup }}</h1>
        <div>
            <button class="button" @click="increment">count++</button>
            <button class="button" @click="reset_counter">reset</button>
        </div>
        <br>
        <input type="text" v-model="message"/>
        <button @click="emitEvent">emit</button>
        <div>{{ response }}</div>
    </div>
</template>

<script>
    import { mapState, mapGetters, mapMutations, mapActions } from 'vuex';

    export default {
        data() {
            return {
                message: '',
                response: 'Server has not yet replied'
            }
        },
        computed: {
            ...mapState(['count']),
            ...mapGetters(['doubleup']),
            halfCount() {
                return this.count / 2;
            },
        },
        sockets: {
            hello_world: function(data) {
                console.log(data);
                this.response = data;
            }
        },
        methods: {
            ...mapMutations(['increment']),
            ...mapActions(['reset_counter']),
            emitEvent() {
                console.log(this.message);
                this.$socket.emit('hello_world', this.message)
            }
        }
    };
</script>