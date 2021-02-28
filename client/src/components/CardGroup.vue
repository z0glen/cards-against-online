<template>
    <b-card-group
        :deck="deck"
        class="p-2 custom-card-group"
        :class="{
            'custom-card-group--selectable': canSelect,
            'custom-card-group--hand': hand
        }"
        @click="handleClick"
    >
        <template v-for="card in cardGroup">
            <Card
                v-bind="card"
                :key="card.id"
                :inHand="hand"
            >
            </Card>
        </template>
    </b-card-group>
</template>

<script>
import Card from "@/components/Card";

export default {
    components: {
        Card,
    },
    props: {
        cardGroup: { type: Array, required: true },
        isJudge: { type: Boolean, required: true },
        canSelect: { type: Boolean, required: true },
        deck: { type: Boolean, default: false },
        hand: { type: Boolean, default: false }
    },
    methods: {
        handleClick() {
            if (this.canSelect) {
                this.$emit('clicked', this.$vnode.key);
            }
        }
    }
}
</script>

<style scoped>
    .custom-card-group {
        border-radius: 5px;
        box-shadow: 0 0 0 2px lightgray;
        display: inline-flex;
        margin: 8px;
    }
    .custom-card-group--selectable {
        cursor: pointer;
    }
    .custom-card-group--hand > :first-child {
        margin: 10px 0px 10px 10px;
    }
    .custom-card-group--hand > :last-child {
        margin: 10px 10px 10px 0px;
    }
</style>