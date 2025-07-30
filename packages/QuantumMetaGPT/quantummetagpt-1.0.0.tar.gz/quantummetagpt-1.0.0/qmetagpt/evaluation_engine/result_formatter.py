import json
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

class ResultFormatter:
    @staticmethod
    def to_json(results, file_path=None):
        """Format evaluation results to JSON"""
        formatted = {
            "counts": results.get('counts'),
            "execution_time": results.get('time'),
            "fidelity": results.get('fidelity'),
            "success": results.get('success')
        }
        json_data = json.dumps(formatted, indent=2)
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(json_data)
            logger.info(f"Results saved to {file_path}")
        return json_data
    
    @staticmethod
    def to_csv(results, file_path=None):
        """Format evaluation results to CSV"""
        import csv
        csv_data = []
        
        # Main metrics
        csv_data.append(["metric", "value"])
        csv_data.append(["execution_time", results.get('time')])
        csv_data.append(["fidelity", results.get('fidelity')])
        csv_data.append(["success", results.get('success')])
        
        # Counts
        counts = results.get('counts', {})
        csv_data.append([])
        csv_data.append(["measurement", "count"])
        for state, count in counts.items():
            csv_data.append([state, count])
        
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
            logger.info(f"Results saved to {file_path}")
        
        return "\n".join([",".join(map(str, row)) for row in csv_data])