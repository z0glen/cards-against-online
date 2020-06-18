<template>
    <div>
        <div class="container text-center">
            <h1>Custom Online Card Player</h1>
            <b-button v-b-modal.create-modal variant="primary" class="button">Create Game</b-button>
            <b-button v-b-modal.join-modal variant="success" class="button">Join Game</b-button>
        </div>
        <b-modal id="create-modal" hide-footer title="Create Game">
            <b-form @submit="createGame">
                <b-form-group
                    id="createName"
                    label="Name:"
                    label-for="name-input"
                    description="How you'll appear to other players."
                >
                    <b-form-input
                        id="name-input"
                        v-model="createForm.name"
                        required
                        placeholder="Enter name"
                    ></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
            </b-form>
        </b-modal>
        <b-modal id="join-modal" hide-footer title="Join Game">
            <b-form @submit="joinGame">
                <b-form-group
                    id="joinName"
                    label="Name:"
                    label-for="name-input"
                    description="How you'll appear to other players."
                >
                    <b-form-input
                        id="name-input"
                        v-model="joinForm.name"
                        required
                        placeholder="Enter name"
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    id="joinRoom"
                    label="Game Code:"
                    label-for="code-input"
                    description="Your unique game code"
                >
                    <b-form-input
                        id="code-input"
                        v-model="joinForm.room"
                        type="password"
                        required
                        placeholder="Enter code"
                    ></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        data() {
            return {
                createForm: {
                    name: "",
                },
                joinForm: {
                    name: "",
                    room: ""
                }
            };
        },
        computed: mapState(['room']),
        watch: {
            room(newState, oldState) {
                console.log(`Updating room from ${oldState} to ${newState}`);
                console.log(newState.id);
                this.$router.push({name: 'Game', params: {code: newState.id}});
            }
        },
        methods: {
            createGame(evt) {
                evt.preventDefault();
                alert(JSON.stringify(this.createForm));
                this.$socket.emit('pingServer', 'PING!');
                this.$socket.emit('create', this.createForm);
                //this.$router.push({name: 'Game', params: {code: this.createForm.room}});
            },
            joinGame(evt) {
                evt.preventDefault();
                alert(JSON.stringify(this.joinForm));
                this.$socket.emit('pingServer', 'PING!');
                this.$socket.emit('join', this.joinForm);
                //this.$router.push({name: 'Game', params: {code: this.joinForm.room}});
            }
        }
    }
</script>

<style scoped>
    .button {
        margin: 10px;
    }
</style>