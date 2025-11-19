<script setup>
import { useForecastStore } from "~/stores/forecast";
import MapComponent from "~/components/MapComponent.vue";

const store = useForecastStore();

// Fetch initial data on first load using the default coordinates
onMounted(() => {
  store.fetchForecast(store.currentLatitude, store.currentLongitude);
});
</script>

<template>
  <NuxtLayout>
    <div class="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
      <header class="mb-8">
        <h1 class="text-4xl font-extrabold text-indigo-700">
          Hyper-Local Forecast Dashboard
        </h1>
        <p class="text-gray-600">72-Hour Air Quality & Allergen Projection</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
          <MapComponent />
        </div>

        <div class="lg:col-span-1 bg-white p-6 shadow-lg rounded-lg">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">
            Location Details
          </h2>
          <p v-if="store.loading" class="text-indigo-500">Loading...</p>
          <p v-else-if="store.error" class="text-red-500">{{ store.error }}</p>
          <div v-else-if="store.forecastData">
            <p class="text-sm text-gray-700">
              Forecast data for nearest point:
            </p>
            <p class="font-mono text-xs text-gray-600">
              Lat: {{ store.forecastData.latitude.toFixed(4) }} | Lon:
              {{ store.forecastData.longitude.toFixed(4) }}
            </p>
            <p class="text-sm text-green-600 mt-2">
              Distance to requested point:
              <span class="font-semibold"
                >{{ store.forecastData.distance_meters }}m</span
              >
            </p>
          </div>
          <p v-else class="text-gray-500">
            Click on the map to load a forecast.
          </p>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>
