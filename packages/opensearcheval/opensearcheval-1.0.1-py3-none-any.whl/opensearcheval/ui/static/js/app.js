// Global app functionality

// Notification system
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
  
    // Set type-specific styles
    notification.className = 'notification';
    if (type === 'success') {
      notification.style.backgroundColor = 'var(--success-color)';
    } else if (type === 'error') {
      notification.style.backgroundColor = 'var(--danger-color)';
    } else if (type === 'warning') {
      notification.style.backgroundColor = 'var(--warning-color)';
    } else if (type === 'info') {
      notification.style.backgroundColor = 'var(--primary-color)';
    }
  
    // Set message
    notification.textContent = message;
  
    // Show notification
    notification.classList.add('show');
  
    // Hide after 5 seconds
    setTimeout(() => {
      notification.classList.remove('show');
    }, 5000);
}

// API helper
const API = {
    baseUrl: '/api',
  
    async get(endpoint) {
      try {
        const response = await fetch(`${this.baseUrl}/${endpoint}`);
      
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
      
        return await response.json();
      } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
      }
    },
  
    async post(endpoint, data) {
      try {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
      
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
      
        return await response.json();
      } catch (error) {
        console.error(`Error posting to ${endpoint}:`, error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
      }
    },
  
    async put(endpoint, data) {
      try {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
      
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
      
        return await response.json();
      } catch (error) {
        console.error(`Error updating ${endpoint}:`, error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
      }
    },
  
    async delete(endpoint) {
      try {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
          method: 'DELETE'
        });
      
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
      
        return await response.json();
      } catch (error) {
        console.error(`Error deleting ${endpoint}:`, error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
      }
    }
};

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function truncateText(text, maxLength = 50) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('OpenSearchEval UI initialized');
});