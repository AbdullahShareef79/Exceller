export enum ProcessingStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export interface Document {
  id: number;
  original_filename: string;
  stored_filename: string;
  output_filename: string | null;
  mime_type: string;
  file_size: string;
  status: ProcessingStatus;
  error_message: string | null;
  created_at: string;
  updated_at: string;
} 