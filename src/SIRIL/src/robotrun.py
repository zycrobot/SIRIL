import rospy
import torch
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import hydra
from .siril.Transformer.transformer import VideoGPTTransformer
import numpy as np
import cv2
from collections import deque


class CellPeelingROSController:
    def __init__(self, cfg):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.cfg = cfg
        self.bridge = CvBridge()

        rospy.init_node("cell_peeling_controller", anonymous=True)
        self.action_publisher = rospy.Publisher(cfg.action_topic, Float32MultiArray, queue_size=10)

   
        rospy.Subscriber(cfg.image_topic, Image, self.image_callback)
        rospy.Subscriber(cfg.traj_topic, Float32MultiArray, self.traj_callback)

   
        self.model = VideoGPTTransformer(cfg.transformer)
        self.model.load_state_dict(torch.load(cfg.model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()

 
        self.image_queue = deque(maxlen=self.cfg.num_frames)
        self.past_actions = deque(maxlen=self.cfg.num_frames - 1)
        self.current_action_dim = cfg.action_dim

    def preprocess_image(self, cv_image):

        cv_image = cv2.resize(cv_image, (self.cfg.image_size, self.cfg.image_size))
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv_image = (cv_image / 127.5 - 1.0).astype(np.float32)
        cv_image = np.transpose(cv_image, (2, 0, 1))
        return torch.tensor(cv_image, dtype=torch.float32).unsqueeze(0).to(self.device)

    def image_callback(self, msg):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            preprocessed_image = self.preprocess_image(cv_image)
            self.image_queue.append(preprocessed_image)
        except Exception as e:
            rospy.logerr(f"Error processing image: {e}")

    def traj_callback(self, msg):

        try:
            traj = torch.tensor(msg.data, dtype=torch.float32).to(self.device)
            if traj.size(0) == self.current_action_dim:
                self.past_actions.append(traj)
        except Exception as e:
            rospy.logerr(f"Error processing trajectory: {e}")

    def predict_action(self):

        if len(self.image_queue) < self.cfg.num_frames or len(self.past_actions) < self.cfg.num_frames - 1:
            rospy.logwarn("Not enough data for prediction yet.")
            return None

 
        images = torch.cat(list(self.image_queue)).unsqueeze(0)  # (1, T, C, H, W)
        past_actions = torch.stack(list(self.past_actions)).unsqueeze(0)  # (1, T-1, action_dim)

    
        with torch.no_grad():
            _, _, predicted_action = self.model.output(images, past_actions, compute_joint=True)

        return predicted_action.squeeze().cpu().numpy()

    def run(self):

        rospy.loginfo("Cell peeling controller started.")
        rate = rospy.Rate(100) 
        while not rospy.is_shutdown():
            predicted_action = self.predict_action()
            if predicted_action is not None:
                action_msg = Float32MultiArray()
                action_msg.data = predicted_action.tolist()
                self.action_publisher.publish(action_msg)
                rospy.loginfo(f"Published action: {predicted_action}")
            rate.sleep()




@hydra.main(config_path="../siril/configs/models/bc", config_name="default")
def main(args):
    CellPeelingROSController(args).run()


if __name__ == '__main__':
    main()