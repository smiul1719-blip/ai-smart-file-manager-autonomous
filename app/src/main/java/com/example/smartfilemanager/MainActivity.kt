package com.example.smartfilemanager

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.graphics.Color
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Description

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    SmartFileManagerScreen()
                }
            }
        }
    }
}

@Composable
fun SmartFileManagerScreen() {
    var searchQuery by remember { mutableStateOf("") }
    val files = remember { mutableStateListOf("Documents", "Images", "Videos", "Downloads", "AI_Generated_Logs.txt", "Project_Notes.pdf") }

    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "AI Smart File Manager", style = MaterialTheme.typography.headlineMedium, modifier = Modifier.padding(bottom = 16.dp))
        
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Search files with AI...") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) }
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        LazyColumn {
            items(files.filter { it.contains(searchQuery, ignoreCase = true) }) {
                FileItem(it)
            }
        }
    }
}

@Composable
fun FileItem(name: String) {
    Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        Row(modifier = Modifier.padding(16.dp), verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
            Icon(
                imageVector = if (name.contains(".")) Icons.Default.Description else Icons.Default.Folder,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.width(16.dp))
            Text(text = name, style = MaterialTheme.typography.bodyLarge)
        }
    }
}