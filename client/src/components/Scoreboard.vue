<template>
    <div>
        <b-table :items="items" :fields="fields" outlined>
            <template v-slot:cell(user)="data">
                {{ data.item.user }}
                <b-icon icon="star-fill" variant="warning" v-if="data.item.isJudge"></b-icon>
            </template>
            <template v-slot:cell(hasPlayedCard)="data">
                <b-icon icon="dash-circle" variant="secondary" v-if="data.item.isJudge"></b-icon>
                <b-icon icon="check" variant="success" v-else-if="data.item.hasPlayedCard"></b-icon>
                <b-icon icon="x" variant="danger" v-else></b-icon>
            </template>
        </b-table>
    </div>
</template>

<script>
    export default {
        props: {
            items: Array
        },
        data() {
            return {
                fields: ['user', 'hasPlayedCard', 'score']
            }
        }
    }
</script>

<style scoped>
    .table {
        margin: 25px 0;
    }
</style>