<template>
    <b-card-group
        deck
        class="p-2 custom-card-group"
        :class="{ canSelect: canSelect }"
        @click="handleClick"
    >
        <template v-for="card in cardGroup">
            <Card
                v-bind="card"
                :key="card.id"
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
        cardGroup: Array,
        isJudge: Boolean,
        canSelect: Boolean,
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
    }

    .canSelect {
        cursor: pointer;
    }
</style>