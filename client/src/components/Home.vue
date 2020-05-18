<template>
    <div>
        <Nav/>
        <br>
        <div class="container">
            <h1 class="text-center">Custom Online Card Player</h1>
            <b-form @submit="joinGame" @reset="onReset">
                <b-form-group
                    id="name"
                    label="Name:"
                    label-for="name-input"
                    description="How you'll appear to other players."
                >
                    <b-form-input
                        id="name-input"
                        v-model="form.name"
                        required
                        placeholder="Enter name"
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    id="code"
                    label="Game Code:"
                    label-for="code-input"
                    description="Your unique game code"
                >
                    <b-form-input
                        id="code-input"
                        v-model="form.code"
                        type="password"
                        required
                        placeholder="Enter code"
                    ></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Join Game</b-button>
            </b-form>
        </div>
    </div>
</template>

<script>
    import Nav from "./Nav";
    export default {
        components: {Nav},
        data() {
            return {
                form: {
                    name: "",
                    code: "",
                }
            }
        },
        methods: {
            joinGame(evt) {
                evt.preventDefault();
                alert(JSON.stringify(this.form));
                this.$router.push({ name: 'Game', params: { code: this.form.code } })
            },
            onReset(evt) {
                evt.preventDefault();
                this.form.name = "";
                this.form.code = "";
            }
        }
    }
</script>

<style scoped>

</style>