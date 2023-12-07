import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import io from 'socket.io-client';

const ChatApp = () => {
  const [socket, setSocket] = useState(null);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [ip, setIp] = useState('');
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  const connectToServer = () => {
    if (name.trim() !== '' && ip.trim() !== '') {
      const newSocket = io(`http://${ip}:5555`);
      setSocket(newSocket);
      setIsConnected(true);
  
      // Enviar el nombre como evento 'name'
      newSocket.emit('name', name);
  
      newSocket.on('message', (msg) => {
        setMessages((prevMessages) => [...prevMessages, msg]);
      });
  
      return () => {
        newSocket.disconnect();
      };
    } else {
      alert('Ingresa un nombre y una IP válidos antes de conectar.');
    }
  };

  const handleConnect = () => {
    const disconnect = connectToServer();

    // Limpieza al desmontar el componente o al reconectar
    return () => {
      setIsConnected(false);
      if (disconnect) {
        disconnect();
      }
    };
  };

  const handleSend = () => {
    if (socket && message.trim() !== '') {
      socket.emit('message', { text: message });
      setMessage('');
    }
  };

  return (
    <View style={styles.container}>
      {!isConnected ? (
        <View style={styles.inputContainer}>
          <Text>Ingresa tu nombre:</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={(text) => setName(text)}
          />
          <Text>Ingresa la IP del servidor:</Text>
          <TextInput
            style={styles.input}
            value={ip}
            onChangeText={(text) => setIp(text)}
          />
          <Button title="Conectar" onPress={handleConnect} />
        </View>
      ) : (
        <View style={styles.chatContainer}>
          <View style={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <Text key={index}>{msg.name}: {msg.text}</Text>
            ))}
          </View>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              value={message}
              onChangeText={(text) => setMessage(text)}
            />
            <Button title="Enviar" onPress={handleSend} />
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 16,
  },
  inputContainer: {
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: 16,
  },
  chatContainer: {
    flex: 1,
  },
  messagesContainer: {
    flex: 1,
    marginBottom: 16,
  },
  input: {
    width: '100%',
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    marginBottom: 8,
  },
});

export default ChatApp;
