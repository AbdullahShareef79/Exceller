import React, { useCallback } from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  useToast,
  Progress,
  Icon,
  Button,
} from '@chakra-ui/react';
import { useDropzone } from 'react-dropzone';
import { FiUpload } from 'react-icons/fi';
import { useMutation } from '@tanstack/react-query';
import { uploadDocument } from '../api/documents';

const Dashboard = () => {
  const toast = useToast();

  const { mutate: upload, isPending } = useMutation({
    mutationFn: uploadDocument,
    onSuccess: () => {
      toast({
        title: 'Document uploaded successfully',
        description: 'Your document is being processed.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Upload failed',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (file) {
        if (!file.name.endsWith('.docx')) {
          toast({
            title: 'Invalid file type',
            description: 'Please upload a .docx file',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
          return;
        }
        upload(file);
      }
    },
    [upload, toast]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
        '.docx',
      ],
    },
    multiple: false,
  });

  return (
    <Box maxW="container.lg" mx="auto">
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="lg" mb={2}>
            Welcome to Exceller
          </Heading>
          <Text color="gray.600">
            Upload your Word documents and convert them to Excel format with ease.
          </Text>
        </Box>

        <Box
          {...getRootProps()}
          p={10}
          border="2px"
          borderColor={isDragActive ? 'brand.500' : 'gray.200'}
          borderStyle="dashed"
          borderRadius="xl"
          bg={isDragActive ? 'brand.50' : 'white'}
          cursor="pointer"
          transition="all 0.2s"
          _hover={{
            borderColor: 'brand.500',
            bg: 'brand.50',
          }}
        >
          <input {...getInputProps()} />
          <VStack spacing={4}>
            <Icon as={FiUpload} w={10} h={10} color="brand.500" />
            <VStack spacing={1}>
              <Text fontSize="lg" fontWeight="medium">
                {isDragActive
                  ? 'Drop your document here'
                  : 'Drag and drop your document here'}
              </Text>
              <Text color="gray.500">or click to browse</Text>
            </VStack>
            <Text fontSize="sm" color="gray.400">
              Supports .docx files up to 16MB
            </Text>
          </VStack>
        </Box>

        {isPending && (
          <Box>
            <Text mb={2}>Uploading document...</Text>
            <Progress size="sm" isIndeterminate colorScheme="brand" />
          </Box>
        )}

        <Box bg="white" p={6} borderRadius="xl" boxShadow="sm">
          <VStack align="stretch" spacing={4}>
            <Heading size="md">Quick Start Guide</Heading>
            <Text>1. Drag and drop your Word document into the upload area</Text>
            <Text>2. Wait for the document to be processed</Text>
            <Text>
              3. Download the converted Excel file from the Documents page
            </Text>
            <Button
              colorScheme="brand"
              size="lg"
              leftIcon={<FiUpload />}
              onClick={() => document.querySelector('input')?.click()}
            >
              Upload Document
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Box>
  );
};

export default Dashboard; 