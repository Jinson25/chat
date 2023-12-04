// App.tsx

import React, {useState, useEffect} from 'react';
import {View, Text, TextInput, Button, FlatList} from 'react-native';
import io from 'socket.io-client';

// Cambia 'http://tu-servidor-de-socket.io' por la URL de tu servidor de Socket.IO
const socket = io('http://tu-servidor-de-socket.io');

interface Message {
  id: string;
  text: string;
}

const App: React.FC = () => {
  const [message, setMessage] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    // Configurar escuchadores de eventos
    socket.on('message', (newMessage: Message) => {
      setMessages(prevMessages => [...prevMessages, newMessage]);
    });

    // Limpiar escuchadores al desmontar el componente
    return () => {
      socket.disconnect();
    };
  }, []);

  const sendMessage = () => {
    if (message.trim() !== '') {
      // Enviar mensaje al servidor
      socket.emit('message', message);

      // Limpiar el campo de mensaje después de enviar
      setMessage('');
    }
  };

  return (
    <View style={{flex: 1, justifyContent: 'center', padding: 16}}>
      <FlatList
        data={messages}
        keyExtractor={item => item.id}
        renderItem={({item}) => <Text>{item.text}</Text>}
      />
      <TextInput
        value={message}
        onChangeText={text => setMessage(text)}
        placeholder="Escribe tu mensaje"
        style={{flexDirection: 'row', marginTop: 16}}
      />
      <Button title="Enviar" onPress={sendMessage} />
    </View>
  );
};

export default App;
