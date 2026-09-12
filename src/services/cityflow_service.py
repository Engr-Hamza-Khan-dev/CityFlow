"""
CityFlow Service Layer

Integrates:
- Member 1's RAG pipeline (retrieval)
- Member 2's agent (AI reasoning & checklist generation)
- Streamlit frontend display

Contract:
- Frontend calls process_question(question: str)
- Backend returns structured response
- Frontend displays results with all fields optional
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

try:
    from agent import generate_checklist
    HAS_AGENT = True
except ImportError:
    HAS_AGENT = False

from rag.pipeline import Member1RAGPipeline


@dataclass
class CityFlowResponse:
    """Structured response from CityFlow pipeline."""

    # Core answer components
    summary: str = ""
    steps: List[Dict[str, Any]] = None  # Each step has requirement, department, cost, timeline, source
    notes: List[str] = None
    
    # Status flags
    confidence: float = 0.0
    is_fallback: bool = False
    
    # Raw data for debugging
    raw_checklist: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize empty lists."""
        if self.steps is None:
            self.steps = []
        if self.notes is None:
            self.notes = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class CityFlowService:
    """Main service orchestrating RAG + AI reasoning."""

    def __init__(self):
        """Initialize the service with RAG pipeline."""
        self.rag = Member1RAGPipeline()
        self._ensure_rag_ready()
        self.has_agent = HAS_AGENT

    def _ensure_rag_ready(self):
        """Ensure RAG index is built."""
        try:
            self.rag.ensure_index()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAG: {str(e)}")

    def process_question(self, question: str) -> CityFlowResponse:
        """
        Main entry point for processing a user question.
        
        Uses Member 2's AI agent (if available) with Member 1's RAG.
        
        Args:
            question: The user's permit question
            
        Returns:
            CityFlowResponse with structured answer
        """
        if not question or not question.strip():
            return CityFlowResponse(
                is_fallback=True,
                summary="Please enter a question.",
            )

        try:
            # Call Member 2's agent if available, otherwise fallback to RAG only
            if self.has_agent:
                return self._process_with_agent(question)
            else:
                return self._process_with_rag_only(question)

        except Exception as e:
            return CityFlowResponse(
                is_fallback=True,
                summary=f"An error occurred: {str(e)}",
            )

    def _process_with_agent(self, question: str) -> CityFlowResponse:
        """Process using Member 2's AI agent (reasoning + checklist generation)."""
        checklist_result = generate_checklist(question)
        
        # Check if we have sufficient evidence
        if not checklist_result.get("sufficient_evidence", False):
            return CityFlowResponse(
                is_fallback=True,
                summary="I couldn't find enough reliable information in the available official sources to answer this confidently.",
                notes=checklist_result.get("notes", []),
                confidence=0.0,
                raw_checklist=checklist_result,
            )
        
        # Convert agent's checklist to our response format
        response = CityFlowResponse(
            summary=checklist_result.get("summary", ""),
            steps=checklist_result.get("checklist", []),
            notes=checklist_result.get("notes", []),
            confidence=1.0,
            is_fallback=False,
            raw_checklist=checklist_result,
        )
        
        return response

    def _process_with_rag_only(self, question: str) -> CityFlowResponse:
        """Fallback: Process using only RAG (when agent is not available)."""
        evidence = self.rag.retrieve(question, k=5)

        if not evidence:
            return CityFlowResponse(
                is_fallback=True,
                summary="No relevant documents found for this question.",
            )

        # Just show the top evidence as a fallback
        response = CityFlowResponse(
            summary=evidence[0]["text"][:500] + "..." if evidence else "Information not found.",
            is_fallback=True,
            confidence=0.3,
        )

        return response


# Singleton instance
_service = None


def get_service() -> CityFlowService:
    """Get or create the singleton service instance."""
    global _service
    if _service is None:
        _service = CityFlowService()
    return _service
