"""
Machine Learning models for network anomaly detection
"""

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import os
from collections import deque
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json


class NetworkAnomalyDetector:
    """
    ML-based anomaly detection using ensemble methods
    """
    
    def __init__(self):
        # Unsupervised models for anomaly detection
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Clustering for pattern recognition
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
        
        # Supervised model for threat classification
        self.threat_classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
        # Feature scaling
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=10)
        
        # Training data buffer
        self.feature_buffer = deque(maxlen=10000)
        self.labeled_threats = deque(maxlen=1000)
        
        # Model state
        self.is_trained = False
        self.feature_names = []
        
        # Performance tracking
        self.detection_history = deque(maxlen=1000)
        
    def extract_features(self, packet: Dict) -> np.ndarray:
        """Extract features from packet for ML processing"""
        features = []
        
        # Time-based features
        hour = datetime.now().hour
        features.extend([
            np.sin(2 * np.pi * hour / 24),  # Cyclic hour encoding
            np.cos(2 * np.pi * hour / 24),
            datetime.now().weekday() / 7.0  # Day of week
        ])
        
        # Packet features
        features.extend([
            self._encode_protocol(packet.get('protocol', 'Unknown')),
            packet.get('size', 100) / 1500.0,  # Normalized packet size
            self._encode_port(packet.get('port', 0)),
            len(packet.get('info', '')) / 100.0  # Info length
        ])
        
        # Device type features
        features.extend([
            self._encode_device_type(packet.get('source_type', 'unknown')),
            self._encode_device_type(packet.get('destination_type', 'unknown'))
        ])
        
        # Traffic pattern features (requires context)
        features.extend(self._get_traffic_pattern_features(packet))
        
        # Pad to ensure consistent feature size
        while len(features) < 15:
            features.append(0.0)
        
        return np.array(features[:15])  # Ensure exactly 15 features
    
    def _encode_protocol(self, protocol: str) -> float:
        """Encode protocol as numeric feature"""
        protocol_map = {
            'TCP': 0.1, 'UDP': 0.2, 'ICMP': 0.3, 'HTTP': 0.4,
            'HTTPS': 0.5, 'SSH': 0.6, 'FTP': 0.7, 'DNS': 0.8,
            'DHCP': 0.9, 'Unknown': 1.0
        }
        return protocol_map.get(protocol, 1.0)
    
    def _encode_port(self, port: int) -> float:
        """Encode port with special handling for common ports"""
        if port == 0:
            return 0.0
        elif port < 1024:  # Well-known ports
            return 0.2 + (port / 1024) * 0.3
        elif port < 49152:  # Registered ports
            return 0.5 + ((port - 1024) / (49152 - 1024)) * 0.3
        else:  # Dynamic ports
            return 0.8 + ((port - 49152) / (65535 - 49152)) * 0.2
    
    def _encode_device_type(self, device_type: str) -> float:
        """Encode device type as numeric feature"""
        device_map = {
            'router': 0.1, 'switch': 0.2, 'firewall': 0.3,
            'server': 0.4, 'workstation': 0.5, 'laptop': 0.6,
            'smartphone': 0.7, 'iot_sensor': 0.8, 'printer': 0.9,
            'unknown': 1.0
        }
        return device_map.get(device_type, 1.0)
    
    def _get_traffic_pattern_features(self, packet: Dict) -> List[float]:
        """Extract traffic pattern features from recent history"""
        # This would normally analyze recent traffic patterns
        # For now, return placeholder features
        return [
            np.random.random(),  # Burst score
            np.random.random(),  # Periodicity score
            np.random.random(),  # Entropy score
            np.random.random()   # Variance score
        ]
    
    def train(self, training_data: Optional[List[Dict]] = None):
        """Train the anomaly detection models"""
        if training_data:
            # Convert training data to features
            for packet in training_data:
                features = self.extract_features(packet)
                self.feature_buffer.append(features)
        
        if len(self.feature_buffer) < 100:
            print("Insufficient training data. Need at least 100 samples.")
            return False
        
        # Prepare training matrix
        X = np.array(list(self.feature_buffer))
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Reduce dimensions
        X_reduced = self.pca.fit_transform(X_scaled)
        
        # Train isolation forest
        self.isolation_forest.fit(X_reduced)
        
        # Train DBSCAN for clustering
        self.dbscan.fit(X_reduced)
        
        # Train threat classifier if we have labeled data
        if self.labeled_threats:
            X_threats = []
            y_threats = []
            for features, label in self.labeled_threats:
                X_threats.append(features)
                y_threats.append(label)
            
            X_threats = np.array(X_threats)
            X_threats_scaled = self.scaler.transform(X_threats)
            X_threats_reduced = self.pca.transform(X_threats_scaled)
            
            self.threat_classifier.fit(X_threats_reduced, y_threats)
        
        self.is_trained = True
        return True
    
    def predict(self, packet: Dict) -> Dict:
        """Predict anomaly and threat level for a packet"""
        features = self.extract_features(packet)
        
        # Add to buffer for continuous learning
        self.feature_buffer.append(features)
        
        if not self.is_trained:
            # Auto-train if we have enough data
            if len(self.feature_buffer) >= 100:
                self.train()
            else:
                # Return default prediction
                return {
                    'is_anomaly': False,
                    'anomaly_score': 0.0,
                    'threat_type': 'none',
                    'confidence': 0.0,
                    'cluster': -1
                }
        
        # Prepare features
        X = features.reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        X_reduced = self.pca.transform(X_scaled)
        
        # Anomaly detection
        anomaly_score = self.isolation_forest.decision_function(X_reduced)[0]
        is_anomaly = self.isolation_forest.predict(X_reduced)[0] == -1
        
        # Clustering
        # For DBSCAN, we need to find nearest cluster
        if hasattr(self.dbscan, 'labels_'):
            distances = np.linalg.norm(X_reduced - self.dbscan.components_, axis=1)
            cluster = np.argmin(distances) if len(distances) > 0 else -1
        else:
            cluster = -1
        
        # Threat classification
        threat_type = 'none'
        confidence = 0.0
        
        if is_anomaly and hasattr(self.threat_classifier, 'classes_'):
            try:
                threat_probs = self.threat_classifier.predict_proba(X_reduced)[0]
                threat_idx = np.argmax(threat_probs)
                threat_type = self.threat_classifier.classes_[threat_idx]
                confidence = threat_probs[threat_idx]
            except:
                pass
        
        result = {
            'is_anomaly': is_anomaly,
            'anomaly_score': float(-anomaly_score),  # Convert to positive score
            'threat_type': threat_type,
            'confidence': float(confidence),
            'cluster': int(cluster)
        }
        
        # Track detection history
        self.detection_history.append({
            'timestamp': datetime.now(),
            'result': result,
            'packet': packet
        })
        
        return result
    
    def add_labeled_threat(self, packet: Dict, threat_label: str):
        """Add labeled threat data for supervised learning"""
        features = self.extract_features(packet)
        self.labeled_threats.append((features, threat_label))
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        model_data = {
            'isolation_forest': self.isolation_forest,
            'dbscan': self.dbscan,
            'threat_classifier': self.threat_classifier,
            'scaler': self.scaler,
            'pca': self.pca,
            'is_trained': self.is_trained
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(model_data, path)
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        if os.path.exists(path):
            model_data = joblib.load(path)
            self.isolation_forest = model_data['isolation_forest']
            self.dbscan = model_data['dbscan']
            self.threat_classifier = model_data['threat_classifier']
            self.scaler = model_data['scaler']
            self.pca = model_data['pca']
            self.is_trained = model_data['is_trained']
            return True
        return False


class DeepLearningDetector:
    """
    Deep learning based detector using LSTM for sequence analysis
    """
    
    def __init__(self):
        self.sequence_length = 20
        self.feature_dim = 15
        self.hidden_dim = 64
        
        # Sequence buffer
        self.sequence_buffer = deque(maxlen=self.sequence_length)
        
        # Initialize model (using numpy for now, can be replaced with TensorFlow/PyTorch)
        self.lstm_weights = self._initialize_lstm_weights()
        self.is_trained = False
        
    def _initialize_lstm_weights(self):
        """Initialize LSTM weights"""
        # Simplified LSTM implementation
        weights = {
            'Wi': np.random.randn(self.feature_dim, self.hidden_dim) * 0.01,
            'Wf': np.random.randn(self.feature_dim, self.hidden_dim) * 0.01,
            'Wo': np.random.randn(self.feature_dim, self.hidden_dim) * 0.01,
            'Wc': np.random.randn(self.feature_dim, self.hidden_dim) * 0.01,
            'Ui': np.random.randn(self.hidden_dim, self.hidden_dim) * 0.01,
            'Uf': np.random.randn(self.hidden_dim, self.hidden_dim) * 0.01,
            'Uo': np.random.randn(self.hidden_dim, self.hidden_dim) * 0.01,
            'Uc': np.random.randn(self.hidden_dim, self.hidden_dim) * 0.01,
            'bi': np.zeros(self.hidden_dim),
            'bf': np.zeros(self.hidden_dim),
            'bo': np.zeros(self.hidden_dim),
            'bc': np.zeros(self.hidden_dim),
            'Wy': np.random.randn(self.hidden_dim, 1) * 0.01,
            'by': np.zeros(1)
        }
        return weights
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def tanh(self, x):
        """Tanh activation function"""
        return np.tanh(x)
    
    def lstm_cell(self, x, h_prev, c_prev):
        """LSTM cell forward pass"""
        # Input gate
        i = self.sigmoid(np.dot(x, self.lstm_weights['Wi']) + 
                        np.dot(h_prev, self.lstm_weights['Ui']) + 
                        self.lstm_weights['bi'])
        
        # Forget gate
        f = self.sigmoid(np.dot(x, self.lstm_weights['Wf']) + 
                        np.dot(h_prev, self.lstm_weights['Uf']) + 
                        self.lstm_weights['bf'])
        
        # Output gate
        o = self.sigmoid(np.dot(x, self.lstm_weights['Wo']) + 
                        np.dot(h_prev, self.lstm_weights['Uo']) + 
                        self.lstm_weights['bo'])
        
        # Cell state
        c_tilde = self.tanh(np.dot(x, self.lstm_weights['Wc']) + 
                           np.dot(h_prev, self.lstm_weights['Uc']) + 
                           self.lstm_weights['bc'])
        
        c = f * c_prev + i * c_tilde
        h = o * self.tanh(c)
        
        return h, c
    
    def predict_sequence(self, sequence: np.ndarray) -> float:
        """Predict anomaly score for a sequence"""
        h = np.zeros(self.hidden_dim)
        c = np.zeros(self.hidden_dim)
        
        # Process sequence through LSTM
        for t in range(len(sequence)):
            h, c = self.lstm_cell(sequence[t], h, c)
        
        # Output layer
        anomaly_score = self.sigmoid(np.dot(h, self.lstm_weights['Wy']) + 
                                    self.lstm_weights['by'])[0]
        
        return anomaly_score


class NetworkMLEngine:
    """
    Main ML engine combining multiple models
    """
    
    def __init__(self):
        self.anomaly_detector = NetworkAnomalyDetector()
        self.deep_detector = DeepLearningDetector()
        
        # Ensemble weights
        self.ensemble_weights = {
            'isolation_forest': 0.4,
            'deep_learning': 0.3,
            'clustering': 0.3
        }
        
    def analyze_packet(self, packet: Dict) -> Dict:
        """Analyze packet using ensemble of models"""
        # Get predictions from anomaly detector
        ml_prediction = self.anomaly_detector.predict(packet)
        
        # Get sequence features for deep learning
        features = self.anomaly_detector.extract_features(packet)
        self.deep_detector.sequence_buffer.append(features)
        
        deep_score = 0.0
        if len(self.deep_detector.sequence_buffer) == self.deep_detector.sequence_length:
            sequence = np.array(list(self.deep_detector.sequence_buffer))
            deep_score = self.deep_detector.predict_sequence(sequence)
        
        # Ensemble prediction
        ensemble_score = (
            self.ensemble_weights['isolation_forest'] * ml_prediction['anomaly_score'] +
            self.ensemble_weights['deep_learning'] * deep_score
        )
        
        # Determine threat level based on ensemble
        if ensemble_score > 0.8:
            threat_level = 'critical'
        elif ensemble_score > 0.6:
            threat_level = 'high'
        elif ensemble_score > 0.4:
            threat_level = 'medium'
        else:
            threat_level = 'low'
        
        return {
            'anomaly_score': ensemble_score * 100,  # Convert to percentage
            'threat_level': threat_level,
            'ml_prediction': ml_prediction,
            'deep_score': deep_score * 100,
            'insights': self._generate_ml_insights(ml_prediction, deep_score),
            'recommendations': self._generate_ml_recommendations(threat_level, ml_prediction)
        }
    
    def _generate_ml_insights(self, ml_pred: Dict, deep_score: float) -> List[str]:
        """Generate insights based on ML predictions"""
        insights = []
        
        if ml_pred['is_anomaly']:
            insights.append(f"🔍 ML detected anomaly (score: {ml_pred['anomaly_score']:.1f})")
        
        if ml_pred['threat_type'] != 'none':
            insights.append(f"🚨 Threat classified as: {ml_pred['threat_type']} ({ml_pred['confidence']:.0%} confidence)")
        
        if deep_score > 0.7:
            insights.append(f"📊 Sequential pattern analysis shows high risk ({deep_score:.0%})")
        
        if ml_pred['cluster'] >= 0:
            insights.append(f"🔗 Traffic belongs to cluster {ml_pred['cluster']}")
        
        return insights
    
    def _generate_ml_recommendations(self, threat_level: str, ml_pred: Dict) -> List[str]:
        """Generate recommendations based on ML analysis"""
        recommendations = []
        
        threat_responses = {
            'ddos': ["Enable rate limiting", "Activate DDoS protection"],
            'malware': ["Isolate affected device", "Run security scan"],
            'exfiltration': ["Block suspicious connections", "Review access logs"],
            'intrusion': ["Check firewall rules", "Enable IDS/IPS"],
            'none': []
        }
        
        if threat_level in ['high', 'critical']:
            recommendations.extend(threat_responses.get(ml_pred['threat_type'], []))
        
        if ml_pred['is_anomaly']:
            recommendations.append("Monitor device behavior closely")
        
        return recommendations[:3]  # Limit to top 3
    
    def train(self, training_data: List[Dict]):
        """Train all models in the ensemble"""
        return self.anomaly_detector.train(training_data)
    
    def save_models(self, directory: str):
        """Save all trained models"""
        os.makedirs(directory, exist_ok=True)
        self.anomaly_detector.save_model(os.path.join(directory, 'anomaly_detector.pkl'))
        # Deep learning model weights can be saved here too
    
    def load_models(self, directory: str):
        """Load pre-trained models"""
        self.anomaly_detector.load_model(os.path.join(directory, 'anomaly_detector.pkl'))