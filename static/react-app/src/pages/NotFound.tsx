import React from 'react';
import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { FiHome } from 'react-icons/fi';

const NotFound = () => {
  return (
    <Box
      minH="calc(100vh - 16rem)"
      display="flex"
      alignItems="center"
      justifyContent="center"
    >
      <VStack spacing={8} textAlign="center">
        <Heading size="4xl" color="brand.500">
          404
        </Heading>
        <VStack spacing={4}>
          <Heading size="xl">Page Not Found</Heading>
          <Text color="gray.600" fontSize="lg">
            Sorry, we couldn't find the page you're looking for.
          </Text>
        </VStack>
        <Button
          as={RouterLink}
          to="/"
          size="lg"
          colorScheme="brand"
          leftIcon={<FiHome />}
        >
          Return Home
        </Button>
      </VStack>
    </Box>
  );
};

export default NotFound; 