package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"

	pb "your/module/path/pb"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type Server struct {
	pb.UnimplementedDiagnosticServiceServer
}

func (s *Server) GetDiagnostic(stream pb.DiagnosticService_GetDiagnosticServer) error {
	var imageBuffer bytes.Buffer
	var clinicalHistory string

	log.Println("received x-ray chunks")

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			return status.Errorf(codes.Internal, "error while receiving x-ray chunks: %v", err)
		}

		if _, err := imageBuffer.Write(req.GetImage()); err != nil {
			return status.Errorf(codes.Internal, "error while buffering image bytes: %v", err)
		}

		if req.GetClinicalHistory() != "" {
			clinicalHistory = req.GetClinicalHistory()
		}

		if req.GetIsLastChunk() {
			break
		}
	}

	if imageBuffer.Len() == 0 {
		return status.Error(codes.InvalidArgument, "no image data received")
	}

	diagnosis, err := getImageDiagnosis(imageBuffer.Bytes(), clinicalHistory)
	if err != nil {
		return err
	}

	diagnosisJSON, err := json.MarshalIndent(diagnosis, "", "  ")
	if err != nil {
		return status.Errorf(codes.Internal, "failed to marshal diagnosis JSON: %v", err)
	}

	// This assumes your proto has a Message field.
	// Better: add a dedicated field like diagnosis_json in your proto.
	return stream.Send(&pb.GetDiagnosticResponse{
		Message: string(diagnosisJSON),
	})
}

func main() {
	// Start your gRPC server here.
	
}
