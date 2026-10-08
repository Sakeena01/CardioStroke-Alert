package com.example.hearthealthcollector

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object HealthApi {

    private const val SERVER_URL =
        "http://10.0.2.2:5000/sync_health"

    suspend fun syncHealthData(
        userId: Int,
        healthData: HealthData
    ): String = withContext(Dispatchers.IO) {

        val json = JSONObject()

        json.put("user_id", userId)

        healthData.heartRate?.let {
            json.put("heart_rate", it)
        }

        healthData.spo2?.let {
            json.put("spo2", it)
        }

        healthData.steps?.let {
            json.put("steps", it)
        }

        healthData.calories?.let {
            json.put("calories", it)
        }

        healthData.distance?.let {
            json.put("distance", it)
        }

        healthData.sleepHours?.let {
            json.put("sleep", it)
        }

        healthData.systolicBP?.let {
            json.put("sbp", it)
        }

        healthData.diastolicBP?.let {
            json.put("dbp", it)
        }

        healthData.bloodGlucose?.let {
            json.put("glucose", it)
        }

        json.put(
            "source",
            healthData.source ?: "Health Connect"
        )

        json.put(
            "device_name",
            healthData.deviceName ?: "boAt ProGear"
        )

        val connection =
            URL(SERVER_URL)
                .openConnection() as HttpURLConnection

        try {

            connection.requestMethod = "POST"

            connection.setRequestProperty(
                "Content-Type",
                "application/json"
            )

            connection.setRequestProperty(
                "Accept",
                "application/json"
            )

            connection.doOutput = true
            connection.connectTimeout = 15000
            connection.readTimeout = 15000

            connection.outputStream.use { output ->

                output.write(
                    json.toString()
                        .toByteArray(Charsets.UTF_8)
                )
            }

            val responseCode =
                connection.responseCode

            val stream =
                if (responseCode in 200..299) {
                    connection.inputStream
                } else {
                    connection.errorStream
                }

            val response =
                stream
                    ?.bufferedReader()
                    ?.use { it.readText() }
                    ?: ""

            if (responseCode !in 200..299) {

                throw Exception(
                    "Server returned $responseCode: $response"
                )
            }

            response

        } finally {

            connection.disconnect()
        }
    }
}

