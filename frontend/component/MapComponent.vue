<script setup>
import { useForecastStore } from "~/stores/forecast";

const store = useForecastStore();
const mapZoom = ref(10);
const tileProvider = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

const center = computed(() => store.mapCenter);

const customIcon = L.icon({
  iconUrl: "/img/marker-icon.png",
  shadowUrl: "/img/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const onMapClick = (event) => {
  const lat = event.latlng.lat;
  const lon = event.latlng.lng;
  console.log(`Map clicked at: ${lat}, ${lon}. Fetching new forecast...`);

  store.fetchForecast(lat, lon);
};
</script>

<template>
  <div class="h-[400px] w-full shadow-lg rounded-lg overflow-hidden relative">
    <div
      v-if="store.loading"
      class="absolute inset-0 bg-white/70 z-20 flex items-center justify-center"
    >
      <div
        class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-700"
      ></div>
      <p class="ml-4 text-indigo-700 font-semibold">Fetching forecast...</p>
    </div>

    <ClientOnly>
      <LMap
        ref="map"
        :zoom="mapZoom"
        :center="center"
        @click="onMapClick"
        :use-global-leaflet="false"
      >
        <LTileLayer
          :url="tileProvider"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />

        <LMarker v-if="store.forecastData" :lat-lng="center" :icon="customIcon">
          <LPopup>
            <div class="text-sm font-semibold">Forecast Point</div>
            <p class="text-xs">Lat: {{ center[0].toFixed(4) }}</p>
            <p class="text-xs">Lon: {{ center[1].toFixed(4) }}</p>
            <p class="text-xs mt-1 text-green-600">
              Data found {{ store.forecastData.distance_meters }}m away.
            </p>
          </LPopup>
        </LMarker>

        <LCircleMarker
          :lat-lng="[store.currentLatitude, store.currentLongitude]"
          :radius="5"
          color="#3b82f6"
          :fill-opacity="0.8"
        />
      </LMap>
    </ClientOnly>
  </div>
</template>
