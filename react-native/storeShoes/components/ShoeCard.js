import React from 'react';
import { View, Text, Image } from 'react-native';
import styles from '../styles'; 

const ShoeCard = ({ item, cardWidth, isDarkTheme }) => {
  return (
    <View style={[styles.card, { width: cardWidth }, isDarkTheme ? styles.darkCard : {}]}>
      <Image source={{ uri: item.url }} style={styles.cardImage} />
      <Text style={[styles.cardTitle, isDarkTheme ? styles.darkText : {}]}>{item.title}</Text>
      <Text style={[styles.cardDescription, isDarkTheme ? styles.darkText : {}]}>{item.thumbnailUrl}</Text>
    </View>
  );
};

export default ShoeCard;