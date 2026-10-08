package com.example.hearthealthcollector

import android.content.Context
import androidx.health.connect.client.HealthConnectClient
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class HealthSyncWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {

        return try {

            // ---------------------------------------------
            // 1. Create Health Connect client
            // ---------------------------------------------

            val healthConnectClient =
                HealthConnectClient.getOrCreate(
                    applicationContext
                )

            // ---------------------------------------------
            // 2. Read all available health data
            // ---------------------------------------------

            val repository =
                HealthRepository(
                    healthConnectClient
                )

            val healthData =
                repository.readAllHealthData(
                    deviceName = "boAt ProGear"
                )

            // ---------------------------------------------
            // 3. Send automatically to Flask
            // ---------------------------------------------

            HealthApi.syncHealthData(
                userId = 1,
                healthData = healthData
            )

            // ---------------------------------------------
            // 4. Success
            // ---------------------------------------------

            Result.success()

        } catch (e: Exception) {

            e.printStackTrace()

            // WorkManager will retry later
            Result.retry()
        }
    }
}