import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  IconButton,
  Skeleton,
  Alert,
  AlertIcon,
  HStack,
  Button,
} from '@chakra-ui/react';
import { FiDownload, FiRefreshCw } from 'react-icons/fi';
import { useQuery } from '@tanstack/react-query';
import { fetchDocuments, downloadDocument } from '../api/documents';
import { ProcessingStatus } from '../types';

const statusColors = {
  [ProcessingStatus.PENDING]: 'yellow',
  [ProcessingStatus.PROCESSING]: 'blue',
  [ProcessingStatus.COMPLETED]: 'green',
  [ProcessingStatus.FAILED]: 'red',
};

const DocumentList = () => {
  const {
    data: documents,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['documents'],
    queryFn: fetchDocuments,
    refetchInterval: (data) => {
      // Refetch every 5 seconds if there are pending or processing documents
      if (
        data?.some((doc) =>
          [ProcessingStatus.PENDING, ProcessingStatus.PROCESSING].includes(
            doc.status
          )
        )
      ) {
        return 5000;
      }
      return false;
    },
  });

  const handleDownload = async (documentId: number) => {
    try {
      await downloadDocument(documentId);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  if (isError) {
    return (
      <Alert status="error">
        <AlertIcon />
        {error instanceof Error ? error.message : 'Failed to load documents'}
      </Alert>
    );
  }

  return (
    <Box maxW="container.xl" mx="auto">
      <VStack spacing={8} align="stretch">
        <HStack justify="space-between">
          <Box>
            <Heading size="lg" mb={2}>
              Documents
            </Heading>
            <Text color="gray.600">
              View and manage your processed documents here
            </Text>
          </Box>
          <Button
            leftIcon={<FiRefreshCw />}
            onClick={() => refetch()}
            colorScheme="brand"
            variant="outline"
          >
            Refresh
          </Button>
        </HStack>

        <Box
          bg="white"
          borderRadius="xl"
          boxShadow="sm"
          overflow="hidden"
          overflowX="auto"
        >
          <Table>
            <Thead>
              <Tr>
                <Th>File Name</Th>
                <Th>Status</Th>
                <Th>Size</Th>
                <Th>Uploaded</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>
              {isLoading ? (
                Array.from({ length: 3 }).map((_, i) => (
                  <Tr key={i}>
                    <Td>
                      <Skeleton height="20px" />
                    </Td>
                    <Td>
                      <Skeleton height="20px" width="100px" />
                    </Td>
                    <Td>
                      <Skeleton height="20px" width="60px" />
                    </Td>
                    <Td>
                      <Skeleton height="20px" width="150px" />
                    </Td>
                    <Td>
                      <Skeleton height="20px" width="40px" />
                    </Td>
                  </Tr>
                ))
              ) : documents?.length === 0 ? (
                <Tr>
                  <Td colSpan={5} textAlign="center" py={8}>
                    <Text color="gray.500">No documents found</Text>
                  </Td>
                </Tr>
              ) : (
                documents?.map((doc) => (
                  <Tr key={doc.id}>
                    <Td fontWeight="medium">{doc.original_filename}</Td>
                    <Td>
                      <Badge colorScheme={statusColors[doc.status]}>
                        {doc.status}
                      </Badge>
                    </Td>
                    <Td>{doc.file_size}</Td>
                    <Td>
                      {new Date(doc.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </Td>
                    <Td>
                      <IconButton
                        aria-label="Download"
                        icon={<FiDownload />}
                        variant="ghost"
                        colorScheme="brand"
                        isDisabled={doc.status !== ProcessingStatus.COMPLETED}
                        onClick={() => handleDownload(doc.id)}
                      />
                    </Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>
        </Box>
      </VStack>
    </Box>
  );
};

export default DocumentList; 