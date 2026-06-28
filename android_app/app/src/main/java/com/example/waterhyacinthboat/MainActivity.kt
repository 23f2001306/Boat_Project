package com.example.waterhyacinthboat

import android.annotation.SuppressLint
import android.app.Activity
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.View
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private lateinit var errorPanel: View
    private lateinit var errorTitle: TextView
    private lateinit var errorMessage: TextView
    private lateinit var retryButton: Button
    private var mainFrameLoadFailed = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.boatWebView)
        errorPanel = findViewById(R.id.errorPanel)
        errorTitle = findViewById(R.id.errorTitle)
        errorMessage = findViewById(R.id.errorMessage)
        retryButton = findViewById(R.id.retryButton)

        setupWebView()
        retryButton.setOnClickListener { loadBoatServer() }
        loadBoatServer()
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.loadWithOverviewMode = true
        webView.settings.useWideViewPort = true

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView,
                request: WebResourceRequest
            ): Boolean {
                return false
            }

            override fun onPageFinished(view: WebView, url: String) {
                if (!mainFrameLoadFailed) {
                    showWebView()
                }
            }

            override fun onReceivedError(
                view: WebView,
                request: WebResourceRequest,
                error: WebResourceError
            ) {
                if (request.isForMainFrame) {
                    mainFrameLoadFailed = true
                    showServerOfflineError()
                }
            }
        }
    }

    private fun loadBoatServer() {
        if (!isNetworkAvailable()) {
            showNoInternetError()
            return
        }

        hideError()
        mainFrameLoadFailed = false
        webView.loadUrl(BOAT_SERVER_URL)
    }

    private fun isNetworkAvailable(): Boolean {
        val connectivityManager = getSystemService(ConnectivityManager::class.java)
        val activeNetwork = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return false

        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
    }

    private fun showWebView() {
        webView.visibility = View.VISIBLE
        errorPanel.visibility = View.GONE
    }

    private fun hideError() {
        webView.visibility = View.VISIBLE
        errorPanel.visibility = View.GONE
    }

    private fun showNoInternetError() {
        webView.visibility = View.GONE
        errorPanel.visibility = View.VISIBLE
        errorTitle.text = getString(R.string.no_internet_title)
        errorMessage.text = getString(R.string.no_internet_message)
    }

    private fun showServerOfflineError() {
        webView.visibility = View.GONE
        errorPanel.visibility = View.VISIBLE
        errorTitle.text = getString(R.string.server_offline_title)
        errorMessage.text = getString(R.string.server_offline_message, BOAT_SERVER_URL)
    }

    companion object {
        private val BOAT_SERVER_URL = BuildConfig.BOAT_SERVER_URL.trimEnd('/')
    }
}
