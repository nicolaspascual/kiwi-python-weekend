<template>
  <div id="app">
    <form>
        <div class="row">
            <label for="departure">Departure</label>
            <datepicker v-model="searchForm.departure_date_from" :format="'yyyy-MM-dd'"></datepicker>
            <label for="return">Return</label>
            <datepicker v-model="searchForm.departure_date_to" :format="'yyyy-MM-dd'"></datepicker>
            <label for="from">From</label>
            <input type="text" v-model="searchForm.source" placeholder="From" />
            <label for="from">To</label>
            <input type="text" v-model="searchForm.destination" placeholder="To" />
            <button @click.prevent="search">Search</button>
        </div>
    </form>
    <div v-if="loading">
        <img src="http://www.nps.tours/public/images/activity/loading.gif" alt="loading">
    </div>
    <div v-else class="row">
        <ul>
            <li v-for="result in searchResults" :key="result.departure">
                <div v-if="Array.isArray(result)">
                    {{ result[0].source }} -> {{ result[1].destination }} (through {{result[0].destination}}), {{ result[0].departure_time }} -> {{ result[1].arrival_time }},
                    {{ result[0].price + result[1].price }} €
                </div>
                <div v-else>
                    {{ result.source }} -> {{ result.destination }}, {{ result.departure_time }} -> {{ result.arrival_time }},
                    {{ result.price }} €
                </div>
            </li>
        </ul>
    </div>
  </div>
</template>

<script>
  import Datepicker from 'vuejs-datepicker'

  export default {
        name: 'main-component',
        data: () => { return {
            loading: false,
            searchForm: {
                departure_date_from: new Date(),
                departure_date_to: new Date(),
                source: 'Madrid',
                destination: 'Barcelona'
            },
            searchResults: []
        };},
        components: {
            'datepicker': Datepicker
        },
        methods: {
            format_date(date) {
                return (date.getYear() + 1900).toString() + '-' + (date.getMonth() + 1).toString().padStart(2, '0') + '-' + date.getDate().toString().padStart(2, '0')
            },
            build_params() {
                return {
                    departure_date_from: this.format_date(this.searchForm.departure_date_from),
                    departure_date_to: this.format_date(this.searchForm.departure_date_to),
                    source: this.searchForm.source,
                    destination: this.searchForm.destination,
                }
            },
            search() {
                this.loading = true
                setTimeout(() => {
                    axios
                        .get('http://0.0.0.0:5000/combinations', { params: this.build_params() })
                        .then(resp => {
                            this.searchResults = resp.data
                            this.loading = false
                        })
                }, 2000);
            }
        },
    }
</script>

<style>
#app {
    width: 1200px;
    margin: auto;
}
</style>
